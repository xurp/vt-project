# -*- coding: utf-8 -*-
'''
download pictures
@auther  wiki zhu
'''
import os
from urllib.request import urlopen
import urllib.request
from urllib.error import URLError, HTTPError
import pymysql
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from io import BytesIO
import socket
import gzip
import random
browserPath = 'C:\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe'
outputDir = 'C:\\Users\\zapposPhoto\\angle-'
parser = 'html5lib'
driver = webdriver.PhantomJS(executable_path=browserPath)
timeout=20
socket.setdefaulttimeout(timeout)
db = pymysql.connect("localhost","root","","zappos")

cursor = db.cursor();
headers  = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Encoding': 'gzip, deflate',
           'Accept-Language': 'en-US,en;q=0.5',
           'Connection': 'keep-alive',
           'Host': 'www.zappos.com',
           'Upgrade-Insecure-Requests': '1',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0'}

#数据表的含义：三张表是准备继续做的，三个18867表，第一个是我目前在下载并且准备下载完的，后两个是id_imgurl下到18867时picture_with_tag到了20340的时候的备份，不一定有用了
#18867_stop是下到18867终止时候的备份。三张ori是wiki给我的。三个20340是目前正在做的并且比较顺利的达到20340时候的备份（三表数量统一）




def thirdCrawler():
    '''
    三级爬虫，根据数据库中url下载图片
    '''
    #从数据库中拿到图片的下载信息
    cursor.execute("select id,imgurl,isdownload from id_imgurl_beforeanglep where isdownload=2")#避免锁的问题，把imgurl拷贝一份出来单独做下载任务
    ############################################由于怀疑并发访问mysql出现插入语句无效的问题，暂时如下操作：
    #zappos要访问3个表，从原始的17950左右开始做，保证三个表的数据同步
    #id_imgurl_18867是只有18867的表，这个表先为了本程序下载img，如果有一天能下载完，停止zappos程序，把本表的isdownload数据同步到最新的id_imgurl表，然后复制id_imgurl表的copy，继续在本程序执行
    #同步的时候可能会遇到18867表的id在id_imgurl表里没有的问题（也可能不会发生），那么可以无视，因为最后分析数据只分析两张表能联表成功且数据完整的数据。
    temp_id_imgUrl_dict = cursor.fetchall()
    for row in temp_id_imgUrl_dict:
        id = str(row[0])
        imgurl = row[1]
        isdownload = row[2]
        print(id)
        #图片没有被下载过
        if isdownload == 2:
            print(id + ": begin")
            try:
                print(imgurl)
                try:
                    req = urllib.request.Request(url=imgurl, headers=headers)
                    response = urllib.request.urlopen(req)
                    html = response.read()
                    compressedStream = BytesIO(html)
                    gzipper = gzip.GzipFile(fileobj=compressedStream)
                    data = gzipper.read()
                    encoding = "gb18030"
                    bsObj = BeautifulSoup(data, "lxml", from_encoding=encoding)
                    time.sleep(3)
                except HTTPError as e:
                    print('The server could not fulfill the request')
                    print('Error code: ', e.code)
                    driver.get(imgurl)
                    bsObj = BeautifulSoup(driver.page_source, parser)
                except URLError as e:
                    print('We failed to reach a server.')
                    print('Reason: ', e.reason)
                    driver.get(imgurl)
                    bsObj = BeautifulSoup(driver.page_source, parser)
                print('bsObj OK')
                try:
                    for i in range(0, 7):
                        if i<1:
                            spanid='angle-'+str(i)
                        else:
                            spanid='angle-p'
                        span = bsObj.find(id=spanid).contents[1]
                        pre1_targetImg = span['style']
                        pre1_targetImg = str(pre1_targetImg)
                        pre2_targetImg = pre1_targetImg.split('(')[1]
                        targetImg = pre2_targetImg.replace('_THUMBNAILS','').replace(')','')
                        #www.zappos.com vs a2.zassets.com
                        targetImg=targetImg.replace('www.zappos.com','a2.zassets.com')
                        targetImg = targetImg.replace(';', '')
                        imgName = outputDir + str(i) + "/" + id + "_" + str(i) + ".png"
                        print(targetImg)
                        print(imgName)
                        if os.path.exists(imgName):
                            print(imgName,'exists!')
                        else:
                            urllib.request.urlretrieve(targetImg, imgName)
                        print(id ,i, ": end")
                    cursor.execute("update id_imgurl_beforeanglep set isdownload=0 WHERE id=" + id)
                    print(1)
                    db.commit()
                except Exception :
                    errorcode=20+i
                    cursor.execute("update id_imgurl_beforeanglep set isdownload="+str(errorcode)+"WHERE id=" + id)
                    if os.path.exists('C:\\Users\\zapposPhoto\\angle-'+str(i)+'\\'+id+'_'+str(i)+'.png'):
                        os.remove('C:\\Users\\zapposPhoto\\angle-'+str(i)+'\\'+id+'_'+str(i)+'.png')
                        print('remove:',i,id)
                    print(22)
                    db.commit()
                    continue
            #except RuntimeError :
            #    cursor.execute("update id_imgurl_beforeanglep set isdownload=2 WHERE id=" + id)
            #    print(33)
            #    db.commit()
            #    continue
                except ReferenceError :
                    continue
            except Exception:
                errorcode = 20 + i
                cursor.execute("update id_imgurl_beforeanglep set isdownload=" + str(errorcode) + " WHERE id=" + id)
                if os.path.exists('C:\\Users\\zapposPhoto\\angle-' + str(i) + '\\' + id + '_' + str(i) + '.png'):
                    os.remove('C:\\Users\\zapposPhoto\\angle-' + str(i) + '\\' + id + '_' + str(i) + '.png')
                    print('remove:', i, id)
                print(222)
                db.commit()
                continue
if __name__ == '__main__':
    if not os.path.exists(outputDir):
        os.makedirs(outputDir)
    while(True):
        thirdCrawler()
        print("Done")
        cursor.close()
        db.close()


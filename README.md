文件说明：（未说明的都是项目原始方法，不用改）
train.py:
第22行 tf.flags.DEFINE_integer("num_labels", 4, "Number of labels for data. (default: 2)")   里面的4是class数
第64行 x_text, y = data_helpers.load_positive_negative_data_files(FLAGS.positive_data_file, FLAGS.negative_data_file) 处理原有的spam_100.utf8和ham_100.utf8
       两个文件，该两个文件把分类下的所有文件（一段话）都放在了同一个utf8文件下
第65行 x_text, y = data_helpers.load_positive_negative_data_files1() 调用了data_helpers里的类，读取四个分类文件夹下的多个txt文件，每个txt文件是一段话
64、65行选一个执行，另一个注释掉

data_helpers.py
load_data_and_labels方法，用于评估结果的eval.py。该方法读取一个utf8文件（目前的测试文件为data目录下的test.utf8，测试文本全都放在了这个文件里）
load_data_and_labels1方法，同上，但是适用于结巴分词的情况下。
load_positive_negative_data_files方法：读取原有的spam_100.utf8和ham_100.utf8。
load_positive_negative_data_files1方法：目前读取四个分类下的文件，并且是分词的情况。如果不要分词，应该是从82行注释到86行（如果不行请自行判断^_^，忘了)

evals.py
第24行 调用4类*100个*300轮  分字版的checkpoint
第26行 调用4类*100个*300轮  分词版的checkpoint
24、26行选一个，另一个注释，当然也能换新的
第69行 测试分字时调用load_data_and_labels
第70行 测试分词时调用load_data_and_labels1

data文件夹
两个utf8文件是项目原始的文件，test文件是测试文件，注意文件里文字间不能有空格（不知道为什么），换行代表另一个样本。例如目前test文件里有五个样本，分别应该是
体育、娱乐、彩票、房产、彩票

runs文件夹
每个小文件夹就是当时的时间戳改编的名字，刚刚运行出来的就是最新的文件夹，里面的prediction.csv是train完，eval完后生成的文件，第一列就是样本，第二列0123分别代表分类结果
体育、娱乐、彩票、房产

总结：
要训练本项目最原始的spam,ham分类情况。train.py的22行4改成2，64行取消注释，65行注释掉；运行train.py，只要checkpoint生成了（在runs目录下的最新文件夹里），就可以
运行eval.py，把24行checkpoint的路径换成runs目录下的最新文件夹，69行取消注释，70行注释掉

要训练分字版的多分类（目前四类），train.py的22行2改成4，64行取消注释，65行注释掉；data_helpers.py的82行到86行注释掉；运行train.py，只要checkpoint生成了（在runs目录下的最新文件夹里），就可以
运行eval.py，把26行checkpoint的路径换成runs目录下的最新文件夹，69行取消注释，70行注释掉

要训练分词版的多分类（目前四类），train.py的22行2改成4，65行取消注释，64行注释掉；data_helpers.py的82行到86行取消注释；运行train.py，只要checkpoint生成了（在runs目录下的最新文件夹里），就可以
运行eval.py，把26行checkpoint的路径换成runs目录下的最新文件夹，70行取消注释，69行注释掉




# nlp-multiclass-text-tf
# 基于cnn的中文文本分类算法

## 简介
参考[IMPLEMENTING A CNN FOR TEXT CLASSIFICATION IN TENSORFLOW](http://www.wildml.com/2015/12/implementing-a-cnn-for-text-classification-in-tensorflow/)实现的一个简单的卷积神经网络，用于中文文本分类任务（此项目使用的数据集是中文垃圾邮件识别任务的数据集），数据集下载地址：[百度网盘](https://pan.baidu.com/s/1i4HaYTB)

## 区别
原博客实现的cnn用于英文文本分类，没有使用word2vec来获取单词的向量表达，而是在网络中添加了embedding层来来获取向量。<br/>
而此项目则是利用word2vec先获取中文测试数据集中各个<strong>字</strong>的向量表达，再输入卷积网络进行分类。

## 运行方法

### 训练
run `python train.py` to train the cnn with the <strong>spam and ham files (only support chinese!)</strong> (change the config filepath in FLAGS to your own)

### 在tensorboard上查看summaries
run `tensorboard --logdir /{PATH_TO_CODE}/runs/{TIME_DIR}/summaries/` to view summaries in web view

### 测试、分类
run `python eval.py --checkpoint_dir /{PATH_TO_CODE/runs/{TIME_DIR}/checkpoints}`<br/>
如果需要分类自己提供的文件，请更改相关输入参数

    如果需要测试准确率，需要指定对应的标签文件(input_label_file):
    python eval.py --input_label_file /PATH_TO_INPUT_LABEL_FILE
    说明：input_label_file中的每一行是0或1，需要与input_text_file中的每一行对应。
    在eval.py中，如果有这个对照标签文件input_label_file，则会输出预测的准确率




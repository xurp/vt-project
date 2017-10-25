# -*- coding: utf-8 -*-

import tensorflow as tf
import numpy as np
import argparse
import data_helpers
import word2vec_helpers
import os
import time

# Parameters
# =======================================================

# Data loading parameters
tf.flags.DEFINE_float("dev_sample_percentage", .1, "Percentage of the training data to use for validation")
#tf.flags.DEFINE_string("positive_data_file", "./data/rt-polaritydata/rt-polarity.pos", "Data source for the positive data.")
#tf.flags.DEFINE_string("negative_data_file", "./data/rt-polaritydata/rt-polarity.neg", "Data source for the negative data.")
tf.flags.DEFINE_string("positive_data_file", "./data/ham_100.utf8", "Data source for the positive data.")
tf.flags.DEFINE_string("negative_data_file", "./data/spam_100.utf8", "Data source for the negative data.")
tf.flags.DEFINE_integer("num_labels", 4, "Number of labels for data. (default: 2)")

# Model hyperparameters
tf.flags.DEFINE_integer("embedding_dim", 128, "Dimensionality of character embedding (default: 128)")
tf.flags.DEFINE_string("filter_sizes", "3,4,5", "Comma-spearated filter sizes (default: '3,4,5')")
tf.flags.DEFINE_integer("num_filters", 128, "Number of filters per filter size (default: 128)")
tf.flags.DEFINE_float("dropout_keep_prob", 0.5, "Dropout keep probability (default: 0.5)")
tf.flags.DEFINE_float("l2_reg_lambda", 0.0, "L2 regularization lambda (default: 0.0)")

# Training paramters
tf.flags.DEFINE_integer("batch_size", 64, "Batch Size (default: 64)")
tf.flags.DEFINE_integer("num_epochs", 200, "Number of training epochs (default: 200)")
tf.flags.DEFINE_integer("evaluate_every", 100, "Evalue model on dev set after this many steps (default: 100)")
tf.flags.DEFINE_integer("checkpoint_every", 100, "Save model after this many steps (defult: 100)")
tf.flags.DEFINE_integer("num_checkpoints", 5, "Number of checkpoints to store (default: 5)")

# Misc parameters
tf.flags.DEFINE_boolean("allow_soft_placement", True, "Allow device soft device placement")
tf.flags.DEFINE_boolean("log_device_placement", False, "Log placement of ops on devices")

# Parse parameters from commands
FLAGS = tf.flags.FLAGS
FLAGS._parse_flags()
print("\nParameters:")
for attr, value in sorted(FLAGS.__flags.items()):
    print("{}={}".format(attr.upper(), value))
print("")

def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--checkpoint_dir', type=str, default='./runs/1508811868/checkpoints/',
                        help='model directory to store checkpointed models')
    parser.add_argument('--text', type=str, default=u'好好笑',
                        help='prime text')
    args = parser.parse_args()
    sample(args)


def sample(args):
    timestamp = str(int(time.time()))
    out_dir = os.path.abspath(os.path.join(os.path.curdir, "runs", timestamp))
    print("Writing to {}\n".format(out_dir))
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    print ('Loading data')
    #x_text, y = data_helpers.load_positive_negative_data_files1()
    # Get embedding vector
    #sentences, max_document_length = data_helpers.padding_sentences(x_text, '<PADDING>')
    #x = np.array(word2vec_helpers.embedding_sentences(sentences, embedding_size=FLAGS.embedding_dim,
                                                      #file_to_save=os.path.join(out_dir, 'trained_word2vec.model')))



    checkpoint_file = tf.train.latest_checkpoint(args.checkpoint_dir)
    graph = tf.Graph()
    with graph.as_default():
        sess = tf.Session()
        with sess.as_default():
            # Load the saved meta graph and restore variables
            saver = tf.train.import_meta_graph("{}.meta".format(checkpoint_file))
            saver.restore(sess, checkpoint_file)

            # Get the placeholders from the graph by name
            input_x = graph.get_operation_by_name("input_x").outputs[0]
            # input_y = graph.get_operation_by_name("input_y").outputs[0]
            dropout_keep_prob = graph.get_operation_by_name("dropout_keep_prob").outputs[0]

            # Tensors we want to evaluate
            predictions = graph.get_operation_by_name("output/predictions").outputs[0]
            #体育 娱乐 彩票 房产
            textlist = ['谁 足 球 踢 得 好 ？',  u'彩 票 中 奖 几 乎 是 不 可 能 的',u'上 海 的 房 价 始 终 居 高 不 下',
                        u'关 晓 彤 主 演 新 版 倚 天 屠 龙 记 让 人 笑 掉 大 牙 '
                        ,u'杜 兰 特 是 勇 士 的 篮 球 运 动 员 ', u'娱 乐 圈 吸 毒 是 常 有 的 事', u'上 海 一 彩 民 中了 二 等 奖',
                        u' 万 达 集 团 再 次 中 标 关键 地 段 的 房 产 开 发 权 '
                        ,u'很 多 观 众 每 晚 准 时 看 体 育 新 闻 ', u'草 莓 音 乐 节 即 将 开 始',
                        u'中 国 福 利 彩 票 是 否 有 黑 幕 不 得 而 知 ',u'房 地 产 行 业 永 远 不 会 倒']
            for i in textlist:
                textlist=[]
                textlist.append(i)
                print(textlist)
                sentences_padded1, max_document_length = data_helpers.padding_sentences(textlist, '<PADDING>')
                raw_x1 = np.array(word2vec_helpers.embedding_sentences(sentences_padded1, embedding_size=FLAGS.embedding_dim,
                                                                       file_to_load='C:/Users/I343039/PycharmProjects/nlp-multiclass-text-tf/runs/1508811868/trained_word2vec.model'))
                predicted_result = sess.run(predictions, {input_x: raw_x1, dropout_keep_prob: 1.0})
                if (predicted_result[0] == 0):
                    print(i + ": 体育")
                elif (predicted_result[0] == 1):
                    print(i + ": 娱乐")
                elif (predicted_result[0] == 2):
                    print(i + ": 彩票")
                elif (predicted_result[0] == 3):
                    print(i + ": 房产")

if __name__ == '__main__':
    main()


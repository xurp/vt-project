# -*- coding: utf-8 -*-

'''
python word2vec_helpers.py input_file output_model_file output_vector_file
'''

# import modules & set up logging
import os
import sys
import logging
import multiprocessing
import time
import json

from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence


def output_vocab(vocab):
    for k, v in vocab.items():
        print(k)


def embedding_sentences(sentences, embedding_size=128, window=5, min_count=5, file_to_load=None, file_to_save=None):
    print('word2vec begin')
    if file_to_load is not None:
        w2vModel = Word2Vec.load(file_to_load)
        print('word2vec 1')
    else:
        print('load is none,using Word2Vec')
        w2vModel = Word2Vec(sentences, size=embedding_size, window=window, min_count=min_count,
                            workers=multiprocessing.cpu_count())
        print('word2vec 2')
        if file_to_save is not None:
            w2vModel.save(file_to_save)
            print('word2vec 3')
    all_vectors = []
    embeddingDim = w2vModel.vector_size
    embeddingUnknown = [0 for i in range(embeddingDim)]
    print('word2vec 4')
    i=0
    for sentence in sentences:
        this_vector = []
        i = i + 1
        print(i)
        for word in sentence:
            if word in w2vModel.wv.vocab:
                this_vector.append(w2vModel[word])
            else:
                this_vector.append(embeddingUnknown)
        all_vectors.append(this_vector)
    print('word2vec ok')
    return all_vectors


def generate_word2vec_files(input_file, output_model_file, output_vector_file, size=128, window=5, min_count=5):
    start_time = time.time()

    # trim unneeded model memory = use(much) less RAM
    # model.init_sims(replace=True)
    model = Word2Vec(LineSentence(input_file), size=size, window=window, min_count=min_count,
                     workers=multiprocessing.cpu_count())
    model.save(output_model_file)
    model.wv.save_word2vec_format(output_vector_file, binary=False)

    end_time = time.time()
    print("used time : %d s" % (end_time - start_time))


def run_main():
    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logger.info("running %s" % ' '.join(sys.argv))

    # check and process input arguments
    if len(sys.argv) < 4:
        print
        globals()['__doc__'] % locals()
        sys.exit(1)
    input_file, output_model_file, output_vector_file = sys.argv[1:4]

    generate_word2vec_files(input_file, output_model_file, output_vector_file)


def test():
    vectors = embedding_sentences([['first', 'sentence'], ['second', 'sentence']], embedding_size=4, min_count=1)
    print(vectors)

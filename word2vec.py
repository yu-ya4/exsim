# -*- coding: utf-8 -*-

from gensim.models import word2vec


if __name__ == '__main__':

    data1 = word2vec.Text8Corpus('./docs/data1.txt')
    model1 = word2vec.Word2Vec(data1, size=200)

    out=model.most_similar(positive=['飲む'], topn=100)
    for x in out:
        print(x[0],x[1])

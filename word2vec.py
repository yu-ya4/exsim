# -*- coding: utf-8 -*-

from gensim.models import word2vec
import sys


if __name__ == '__main__':

    data = word2vec.Text8Corpus('./docs/data2.txt')
    model = word2vec.Word2Vec(data, size=200, window=15)
    model.save('test3.model')

    action_list = []
    f = open('./actions.txt', 'r')
    for line in f:
        action = line.replace('\n', '')
        action = action.replace('"', '')
        action_list.append(action)
    f.close()

    print('ok')

    for query in sys.stdin:
        if query in action_list:
            # similar_actions = []
            out=model.most_similar(positive=[query], topn=10000)
            for x in out:
                if x[0] in action_list:
                    print(x[0],x[1])

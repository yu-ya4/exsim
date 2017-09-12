# -*- coding: utf-8 -*-

from gensim.models import word2vec
import sys
import os
sys.path.append('../act-geo-matrix')
from experience import Experience, Experiences
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

def show_similar_actions(model, action_list, action):
    if action in action_list:
        out = model.most_similar(positive=[action], topn=100000)
        for x in out:
            if x[0] in action_list:
                print(x[0], x[1])
    else:
        print('There is not such action.')

def show_similar_actions_symbol(model, action_list, action):
    if action in action_list:
        index = action_list.index(action)
        symbol = 'action_replace_number_' + str(index)
        out = model.most_similar(positive=[symbol], topn=100000)
        for x in out:
            l = x[0].split('_')
            if len(l) == 4:
                if l[3] != '':
                    act_i = int(l[3])
                    print(action_list[act_i], x[1])
    else:
        print('There is not such action.')

def get_similar_actions(model, action_list, action):
    result = []
    try:
        if action in action_list:
            out = model.most_similar(positive=[action], topn=100000)
            for x in out:
                if x[0] in action_list:
                    result.append([x[0], x[1]])
        else:
            print('There is not such action.')

        return result
    except:

        return result

def get_similar_experience_symbols(model, experiences, verb, modifiers):
    results = []

    index = experiences.get_index(verb, modifiers)
    if index is not None:
        symbol = 'experience_replace_number_' + str(index)
        try:
            out = model.most_similar(positive=[symbol], topn=1000000)
            for x in out:
                l = x[0].split('_')
                if len(l) == 4:
                    if l[3] != '':
                        exp_i = int(l[3])
                        results.append([experiences.experiences[exp_i].modifiers[0], x[1]])
        except:
            results.append([])

    else:
        print('There is not such action.')

    return results

if __name__ == '__main__':

    # r_windows = ['5', '10', '15', '20', '25', '30', '50']
    r_windows = ['10']
    # r_window = '5'
    # w_windws = ['5', '10', '15', '20', '30', '40', '50']
    w_windws = ['5', '10', '15']
    # w_windws = ['5']

    #
    # for r_window in r_windows:
    #     data = word2vec.Text8Corpus('../../data/docs/test/test-divided-replaced-10.txt')
    #     for window in w_windws:
    #         model = word2vec.Word2Vec(data, size=200, window=int(window), min_count=5)
    #         model.save('../../data/models/test/drink_' + r_window + '_' + window + '_three.model')
    # exit()

    experiences = Experiences()
    experiences.read_experiences_from_database('chie-extracted2')

    for r_window in r_windows:
        for window in w_windws:
            model = word2vec.Word2Vec.load('../../data/models/test/drink_' + r_window + '_' + window + '_three.model')
            file_dir = '../../data/similarities/test/drink_' + r_window + '_' + window + '_three/'
            if not os.path.exists(file_dir):
                os.makedirs(file_dir)

            for experience in experiences.experiences:
                results = get_similar_experience_symbols(model, experiences, experience.verb, experience.modifiers)
                filename = file_dir + experience.modifiers[0] + '.txt'
                try:
                    f_r = open(filename, 'w')
                    if results[0]:
                        for result in results:
                            line = result[0] + ':' + str(result[1]) + '\n'
                            f_r.write(line)
                    f_r.close()
                except:
                    continue
    exit()

    for query in sys.stdin:
        action = query.replace('\n', '')
        show_similar_actions_symbol(model, action_list, action)


    # model = word2vec.Word2Vec.load('./models/0_0_drink.model')
    # out = model.most_similar(positive=['ちょっと飲む'], topn=100000)
    # for x in out:
    #     if x[0] in action_list:
    #         print(x[0], x[1])
    # exit()
    #
    # for query in sys.stdin:
    #     action = query.replace('\n', '')
    #     show_similar_actions(model, action_list, action)

    #
    # exit()
    # data = word2vec.Text8Corpus('./docs/tabelog/1_1_tabe_data_replace.txt')
    # model = word2vec.Word2Vec(data, size=200, window=15)
    # model.save('./models/1_1_tabe_replace.model')
    #
    # exit()

    # for query in sys.stdin:
    #     if query in action_list:
    #         # similar_actions = []
    #         out=model.most_similar(positive=[query], topn=10000)
    #         for x in out:
    #             if x[0] in action_list:
    #                 print(x[0],x[1])

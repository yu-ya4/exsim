#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

from document import Document
# from gensim.models import word2vec
import sys
sys.path.append('../mygensim')
from gensim.models import word2vec as myword2vec

if __name__ == '__main__':

    # doc = Document()
    # doc.read_experience_list('chie-extracted2')
    # # 分かち書きされた文章を読み込みメンバ変数に保存.
    # doc.read_document('../../data/docs/0918/reviews_divided.txt')
    # # 「飲む」という語に注目．「飲む」の10語以内にある経験をなす語(experiencesに含まれる語)を記号に置き換える．
    # doc.replace_experiences('飲む', 10)
    # doc.write_document('../../data/docs/0918/reviews_replaced_10.txt')
    # exit()

    # doc = Document()
    # doc.read_action_list('../act-geo-matrix/actions/20170816/20170816test-actions.txt')
    # doc.read_document('./docs/tabelog/20170816/reviews_divided.txt')
    # # words = ['カウンター' 'ちょっと', 'オシャレ']
    #
    # # doc.weight_words(4, words)
    # doc.replace_actions('飲む', 15)
    # doc.write_document('./docs/tabelog/20170816/reviews_actions_20170816test_replaced_15.txt')
    # exit()
    # doc = Document()
    # # doc.make_text_file_from_database(0, '../../data/docs/0912/reviews.txt')
    # # doc.make_text_file_from_database(1, '../../data/docs/0912/restaurant_prs.txt')
    # doc.make_text_file_from_database(2, '../../data/docs/0912/reviews-restaurant_prs.txt')
    # exit()

    # doc = Document()
    # # doc.make_document('../../data/docs/0912/reviews.txt')
    # # doc.write_document('../../data/docs/0912/reviews_divided.txt')
    #
    # # doc.make_document('../../data/docs/0912/restaurant_prs.txt')
    # # doc.write_document('../../data/docs/0912/restaurant_prs_divided.txt')
    #
    # doc.make_document('../../data/docs/0912/reviews-restaurant_prs.txt')
    # doc.write_document('../../data/docs/0912/reviews-restaurant_prs_divided.txt')
    # exit()

    # doc = Document()
    # doc.read_experience_list('chie-extracted2')

    # doc.read_document('../../data/docs/0912/reviews_divided.txt')
    # doc.replace_experiences('飲む', 10)
    # doc.write_document('../../data/docs/0912/reviews_divided_replaced_10.txt')

    # doc.read_document('../../data/docs/0912/restaurant_prs_divided.txt')
    # doc.replace_experiences('飲む', 10)
    # doc.write_document('../../data/docs/0912/restaurant_prs_divided_replaced_10.txt')
    #
    # doc.read_document('../../data/docs/0912/reviews-restaurant_prs_divided.txt')
    # doc.replace_experiences('飲む', 10)
    # doc.write_document('../../data/docs/0912/reviews-restaurant_prs_divided_replaced_10.txt')
    # exit()



    # # doc.read_document('../../data/docs/0912/restaurant_prs_divided_replaced_5.txt')
    # # doc.weight_experiences(2)
    # # doc.write_document('../../data/docs/0912/restaurant_prs_divided_replaced_5_three.txt')
    #
    # doc.read_document('../../data/docs/0912/reviews-restaurant_prs_divided_replaced_10.txt')
    # doc.weight_experiences(2)
    # doc.write_document('../../data/docs/0912/reviews-restaurant_prs_divided_replaced_10_three.txt')
    #
    exit()

    # words = ['カウンター' 'ちょっと', 'オシャレ']
    # doc.weight_words(4, words)

    # doc = Document()
    # doc.read_experience_list('chie-extracted2')
    # doc.read_document('../../data/docs/test/test-divided-replaced-10.txt')
    # doc.get_words_around_experiences(15)
    # doc.show_words_around_experience('ちょっと')
    # exit()



    # all_text = ''
    # fw = open('../act-geo-matrix/reviews/search_test/all_bodies.txt', 'w')
    #
    # for action in doc.action_list:
    #     f = open('../act-geo-matrix/reviews/search_test/' + action + '/bodies.txt', 'r')
    #     for line in f:
    #         fw.write(line)
    #         body = line.replace('/n', '')
    #         all_text += body
    #     f.close()
    #
    # fw.close()

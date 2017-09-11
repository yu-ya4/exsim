#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

from document import Document

if __name__ == '__main__':


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
    # doc.make_text_file_from_database(0, '../../data/docs/test/test.txt')
    # exit()

    # doc = Document()
    # doc.make_document('../../data/docs/test/test.txt')
    # # words = ['カウンター' 'ちょっと', 'オシャレ']
    # doc.write_document('../../data/docs/test/test-divided.txt')
    # exit()

    # doc = Document()
    # doc.read_experience_list('chie-extracted2')
    # doc.read_document('../../data/docs/test/test-divided.txt')
    # doc.replace_experiences('飲む', 10)
    # doc.write_document('../../data/docs/test/test-divided-replaced-10.txt')
    # exit()

    # doc = Document()
    # doc.read_experience_list('chie-extracted2')
    # doc.read_document('../../data/docs/test/test-divided-replaced-10.txt')
    # doc.weight_experiences(2)
    # doc.write_document('../../data/docs/test/test-divided-replaced-10-three.txt')
    # exit()
    # words = ['カウンター' 'ちょっと', 'オシャレ']

    # doc.weight_words(4, words)

    doc = Document()
    doc.read_experience_list('chie-extracted2')
    doc.read_document('../../data/docs/test/test-divided-replaced-10.txt')
    doc.get_words_around_experiences(15)
    doc.show_words_around_experience('ちょっと')
    exit()



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

#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

from document import Document

if __name__ == '__main__':
    doc = Document()
    doc.read_action_list('../act-geo-matrix/actions/action_飲む_extended.txt')
    # doc.make_document('../act-geo-matrix/reviews/search_test/大人数で朝まで飲む/bodies.txt')
    doc.make_document('../act-geo-matrix/reviews/yolp/kyoto/bodies.txt')
    doc.replace_actions('飲む', 100)
    doc.write_document('../act-geo-matrix/reviews/yolp/kyoto/all_bodies_replaced_100.txt')
    # print(doc.document)
    # rep_dic = doc.make_replace_dict()
    # print(rep_dic)

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

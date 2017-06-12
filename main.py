#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

from document import Document

if __name__ == '__main__':
    doc = Document()
    doc.read_action_list('../act-geo-matrix/actions/20170607飲むcut.txt')
    doc.read_document('../act-geo-matrix/reviews/20170607/all_text_飲む_replaced_50.txt')
    doc.weight_actions(2)
    doc.write_document('../act-geo-matrix/reviews/20170607/all_text_飲む_replaced_50_three.txt')
    exit()

    # doc5 = Document()
    # doc5.read_action_list('../act-geo-matrix/actions/20170607飲むcut.txt')
    # doc5.make_document('../act-geo-matrix/reviews/20170607/all_text_飲む.txt')
    # doc5.replace_actions('飲む', 5)
    # doc5.write_document('../act-geo-matrix/reviews/20170607/all_text_飲む_replaced_5.txt')
    #
    # doc10 = Document()
    # doc10.read_action_list('../act-geo-matrix/actions/20170607飲むcut.txt')
    # doc10.make_document('../act-geo-matrix/reviews/20170607/all_text_飲む.txt')
    # doc10.replace_actions('飲む', 10)
    # doc10.write_document('../act-geo-matrix/reviews/20170607/all_text_飲む_replaced_10.txt')
    #
    # doc15 = Document()
    # doc15.read_action_list('../act-geo-matrix/actions/20170607飲むcut.txt')
    # doc15.make_document('../act-geo-matrix/reviews/20170607/all_text_飲む.txt')
    # doc15.replace_actions('飲む', 15)
    # doc15.write_document('../act-geo-matrix/reviews/20170607/all_text_飲む_replaced_15.txt')
    #
    # doc20 = Document()
    # doc20.read_action_list('../act-geo-matrix/actions/20170607飲むcut.txt')
    # doc20.make_document('../act-geo-matrix/reviews/20170607/all_text_飲む.txt')
    # doc20.replace_actions('飲む', 20)
    # doc20.write_document('../act-geo-matrix/reviews/20170607/all_text_飲む_replaced_20.txt')
    #
    # doc25 = Document()
    # doc25.read_action_list('../act-geo-matrix/actions/20170607飲むcut.txt')
    # doc25.make_document('../act-geo-matrix/reviews/20170607/all_text_飲む.txt')
    # doc25.replace_actions('飲む', 25)
    # doc25.write_document('../act-geo-matrix/reviews/20170607/all_text_飲む_replaced_25.txt')
    #
    # doc50 = Document()
    # doc50.read_action_list('../act-geo-matrix/actions/20170607飲むcut.txt')
    # doc50.make_document('../act-geo-matrix/reviews/20170607/all_text_飲む.txt')
    # doc50.replace_actions('飲む', 50)
    # doc50.write_document('../act-geo-matrix/reviews/20170607/all_text_飲む_replaced_50.txt')


    # doc = Document()
    # doc.read_action_list('../act-geo-matrix/actions/action_飲む_extended.txt')
    # # doc.make_document('../act-geo-matrix/reviews/search_test/大人数で朝まで飲む/bodies.txt')
    # doc.make_document('../act-geo-matrix/reviews/yolp/kyoto/bodies.txt')
    # doc.replace_actions('飲む', 100)
    # doc.write_document('../act-geo-matrix/reviews/yolp/kyoto/all_bodies_replaced_100.txt')
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

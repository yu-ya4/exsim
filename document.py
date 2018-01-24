# -*-coding: utf-8 -*-

import MeCab
import sys
import MySQLdb
import os
import traceback
import sys
import re
import numpy as np
from collections import Counter
from egmat.experience import Experience, Experiences
from .dbconnection import get_db_connection
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


def make_text_file_from_database(mode, conditions, output_filename):
    '''
    make text file from database

    Args:
        mode: int
            0 -> reviews, 1 -> restaurant prs, 2-> reviews and restaurant prs
        conditions: str
            where res.pal="kyoto" limit 10
        output_filename: str
    '''

    try:
        db_connection = get_db_connection()
        cursor = db_connection.cursor()

        sql = '''
            SELECT res.restaurant_id, res.pr_comment_title, res.pr_comment_body, rev.id, rev.title, rev.body
            from restaurants as res left join reviews as rev on res.restaurant_id = rev.restaurant_id
            '''
        sql += conditions

        cursor.execute(sql)
        result = cursor.fetchall()

        with open(output_filename, 'w') as f:
            # 1行に1地物の店舗情報(title+body) or 1つのレビュー(title+body)
            restaurant_id = 0
            for row in result:
                if mode != 0:
                    if restaurant_id != row[0]:
                        restaurant_id = row[0]
                        pr_title = '' if row[1] is None or row[1] == '' else row[1]
                        pr_body = '' if row[2] is None or row[2] == '' else row[2]
                        pr = pr_title + pr_body + '\n'
                        f.write(pr)
                if mode != 1:
                    review_title = '' if row[4] is None or row[4] == '' else row[4]
                    review_body = '' if row[5] is None or row[5] == '' else row[5]
                    review = review_title + review_body
                    review = review.replace('\n', '')
                    review = review.replace('\r', '')
                    f.write(review + '\n')
    except MySQLdb.Error as e:
        print('MySQLdb.Error: ', e)

    except Exception as e:
        traceback.print_exc()
        print(e)

    cursor.close()
    db_connection.close()

def remove_urls(text):
    '''
    Remove urls from text

    Args:
        text: str
    Returns:
        str
    '''
    pattern = r'https?://[\w/:%#\$&\?\(\)~\.=\+\-]+'
    text = re.sub(pattern, '', text)
    return text

def remove_unnecessary_expressions(text):
    '''
    Remove unnecessary expressions from text

    Args:
        text: str
    Returns:
        str
    '''
    patterns = [
        r'DAmb\.Ad\.GDN.*html\'}\);',
        r'varblogCommentType=.*;',
        r'(\(|（)笑(\)|）)',
        # r'[0-9|０-９|,|，]+円',
        # r'[0-9|０-９|一二三四五六七八九十百]+時間?半?',
        # r'[0-9|０-９|一二三四五六七八九十百]+分',
        # r'[0-9|０-９]+[:|：][0-9|０-９]+',
        r'[\(\)（）\^▽⌒\*＊\-_\+\:\?!\？\！\.．.。，、;；￣@＠#＃%％\$＄&＆♪/／＼\\≧≦○◯◎●◉❍✕✗✖´∀`❀ﾉ]'
    ]
    for pattern in patterns:
        text = re.sub(pattern, '', text)
    return text

def normalyze_dictionary_by_maximum(dic):
    '''
    Args:
    dict: dic{str: float}
    '''
    maximum = sorted(dic.items(), key=lambda x: x[1], reverse=True)[0][1]
    if maximum == 0:
        return dic
    for key, val in dic.items():
        dic[key] = val/maximum

    return dic

def diveide_texts(input_filename, output_filename):
        '''
        Args:
            input_filename: str
                入力するテキストファイル名(分かち書きされていない)
            output_filename: str
                出力先のテキストファイル名(分かち書きされている)

        名詞，動詞，形容詞，副詞のみ
        原形で分かち書き
        '''
        mt = MeCab.Tagger("-Ochasen")
        with open(input_filename, 'r') as in_f:
            with open(output_filename, 'w') as out_f:
                for line in in_f:
                    line = remove_unnecessary_expressions(line)
                    line = remove_urls(line)
                    line = line.replace('\n', '')
                    res = mt.parseToNode(line)
                    sentence = ''
                    while res:
                        arr = res.feature.split(",")
                        if arr[0] == '名詞' or arr[0] == '動詞' or arr[0] == '副詞' or arr[0] == '形容詞':
                            if arr[6] == '*':
                                if sentence == '':
                                    sentence += res.surface
                                else:
                                    sentence += ' ' + res.surface
                            else:
                                if sentence == '':
                                    sentence += arr[6]
                                else:
                                    sentence += ' ' + arr[6]
                        res = res.next
                    # print(sentence)
                    out_f.write(sentence + '\n')

class Document():
    '''
    represents a document
    '''
    def __init__(self, words=[], document_id=0):
        '''
        words: list[str]
            ['今日', 'は', 'いい', '天気', 'です', '。', '本当', ' です', 'ね', '飲み', 'たい'], ...]
        '''
        self.document_id = document_id
        self.words = words
        self.words_frequencies_around_experiences = {}
        self.words_indexes_around_experiences = {}
        self.words_frequencies_dictionary = {}


    def get_words_frequencies_around_target(self, target, window=5):
        '''
        対象語の周辺語を取得
        Args:
            target: str
                対象とする語
            window: int
                周辺語をとるサイズ
        Returns:
            words_frequencies_around_target: Dictionary<str, int>
                周辺語をkey，出現頻度をvalueとした辞書
            words_indexes_around_target: Dictionary<str, List<int>>
                    対象語のインデックスをkey，周辺語のインデックスのリストをvalueとした辞書
                {対照語のインデックス: [indexes]}
        '''
        words_frequencies_around_target = {}
        words_indexes_around_target = {}

        # 文書中の対象語のインデックスを取得
        target_indexes = [i for i, word in enumerate(self.words) if word == target]

        # 文書中に対象語があれば周辺語を取得
        if target_indexes:
            length = len(self.words)

            for i in target_indexes:
                indexes = []

                j = i - 1
                while 1:
                    # 対象語よりウィンドウサイズ以内の語のインデックスを取得
                    # 文書の始まりに気をつける
                    if j < 0 or j == i - window - 1:
                        break
                    indexes.append(j)
                    j -= 1

                j = i + 1
                while 1:
                    # 文章の終わりに気をつける
                    if j >= length or j == i + window + 1:
                        break
                    indexes.append(j)
                    j += 1

                for index in indexes:
                    # 周辺語の出現頻度を値とした辞書を作成
                    word = self.words[index]
                    if word in words_frequencies_around_target:
                        words_frequencies_around_target[word] += 1
                    else:
                        words_frequencies_around_target[word] = 1

                # 対象語のインデックスをキーとし，
                # 対象語に対する周辺語のインデックスを値とした辞書を作成
                key = str(i)
                words_indexes_around_target[key] = indexes

        return words_frequencies_around_target, words_indexes_around_target

    def replace_experiences_with_symbols(self, target_verb, window, replace_dict):
        '''
        target_verb("飲む"等)の周辺に，経験を成す語がすべて含まれる場合，それらを記号に置き換える．

        Args:
            target_verb: 対象となる経験の動詞部分を表す語．'飲む'等の動詞を想定．
            window: windowサイズ
        '''
        # target_verbをキーワードから除く
        for symbol, keywords in replace_dict.items():
            if target_verb in keywords:
                keywords.remove(target_verb)

        # 語の原形を比較するため
        mt = MeCab.Tagger("-Ochasen")

        # 周辺語をsymbolに置換したtarget_verbのインデックスを記憶する辞書
        # {'experience_replace_number_0': [5, 13], ...}
        replaced_target_verb_indexes = {}
        # self.words = ['天気', 'が', '良い', 'ので', '一', '人', 'で', 'ちょっと', '出かけて', '安く','飲む', 'こと', 'する', 'さあ', '親', 'と', 'ちょっと', '飲む', '。', '安い', 'し', '美味い']

        _, words_indexes_around_target_verb = self.get_words_frequencies_around_target(target_verb, window)
        for target_verb_index, indexes in words_indexes_around_target_verb.items():
            for symbol, keywords in replace_dict.items():
                # keywordがすべて含まれているか調べる
                keywords_in = True
                temp = []
                for keyword in keywords:
                    if not keywords_in:
                        break
                    for i in indexes:
                        # もともと原形やからいらなくね？
                        # res = mt.parseToNode(self.words[sen_i][i])
                        # res = res.next
                        # arr = res.feature.split(",")
                        # if arr[6] == '*':
                        #     original_form = res.surface
                        # else:
                        #     original_form = arr[6]
                        # if original_form == keyword:
                        #     temp.append(i)
                        #     keywords_in = True
                        #     break
                        # else:
                        #     keywords_in = False
                        if self.words[i] == keyword:
                            temp.append(i)
                            keywords_in = True
                            break
                        else:
                            keywords_in = False

                # keywordがすべて含まれていれば
                if keywords_in:
                    for i in temp:
                        # 記号に置換
                        self.words[i] = symbol

                    if symbol in replaced_target_verb_indexes:
                        replaced_target_verb_indexes[symbol].append(int(target_verb_index))
                    else:
                        replaced_target_verb_indexes[symbol] = [int(target_verb_index)]
                else:
                    continue

        # target_verbもsymbolに置き換える
        # ずれた分考えられてないけど...
        for symbol, target_verb_indexes in replaced_target_verb_indexes.items():
            for target_verb_index in target_verb_indexes:
                if self.words[target_verb_index] == target_verb:
                    # target消去
                    self.words.pop(target_verb_index)
                    self.words.insert(target_verb_index, symbol)
                else:
                    self.words.insert(target_verb_index, symbol)


    def get_words_frequencies_around_experiences(self, window, replace_dict):
        '''
        リスト中の経験の周辺語を得る
            ex.) self.words_around_experiences['ゆっくり飲む'] = {'バー': 10, ...}

        Args:
            window: int
                周辺語をとるサイズ
            replace_dict: dict{str: list[str]}

            {
                'experience_replace_number_0': ['少し', '飲む'],
                'experience_replace_number_1': ['女性', '飲む']
                'experience_replace_number_2': ['一', '人', '飲む']
                ...
            }
        '''
        # 初期化
        self.words_frequencies_around_experiences = {}
        self.words_indexes_around_experiences = {}

        i = 0
        for experience_symbol, exp in replace_dict.items():
            exp = ''.join(exp)
            words, indexes = self.get_words_frequencies_around_target(experience_symbol, window)
            self.words_frequencies_around_experiences[exp] = words
            self.words_indexes_around_experiences[exp] = indexes
            i+=1

class Documents():
    def __init__(self):
        '''
        documents: list[Document]
        '''
        self.documents = []
        self.words_frequencies_around_experiences = {}
        self.experiences = Experiences()
        self.replace_dict = {}
        self.all_words_frequencies_dictionary = {}
        self.all_documents_weight = {}

    def read_documents(self, filename):
        '''
        Args:
            filename: str
                分かち書きされた文書ファイル
        '''
        with open(filename, 'r') as f:
            i = 0
            for line in f:
                line = line.replace('\n', '')
                sentence = line.split(' ')
                document = Document(sentence, i)
                self.documents.append(document)
                i += 1

    def read_experience_list(self, label):
        '''
        Args:
            label: str
                ex: 'chie-extracted2'
        '''
        self.experiences.__init__()
        self.experiences.read_experiences_from_database(label)


    def get_words_frequencies_around_experiences(self, window=5):
        '''
        リスト中の経験の周辺語を得る
            ex.) self.words_around_experiences['ゆっくり飲む'] = {'バー': 10, ...}

        Args:
            window: int
                周辺語をとるサイズ
        '''
        # 初期化
        self.words_frequencies_around_experiences = {}
        self.words_indexes_around_experiences = {}

        for document in self.documents:
            document.get_words_frequencies_around_experiences(window, self.replace_dict)
            # print(document.words_frequencies_around_experiences)
            for exp, words_frequencies in document.words_frequencies_around_experiences.items():
                exp = ''.join(exp)
                if exp not in self.words_frequencies_around_experiences:
                    self.words_frequencies_around_experiences[exp] = words_frequencies
                else:
                    self.words_frequencies_around_experiences[exp] = dict(Counter(self.words_frequencies_around_experiences[exp]) + Counter(words_frequencies))

    #
    # def show_words_around_experience(self, mod):
    #     '''
    #     特定の行動名の周辺語を出現頻度順に表示させる
    #     Args:
    #         mod: str
    #     '''
    #     print(sorted(self.words_around_experiences[mod].items(), key = lambda x: x[1]))

    def replace_experiences_with_symbols(self, target_verb, window=5):
        for document in self.documents:
            document.replace_experiences_with_symbols(target_verb, window, self.replace_dict)

    def make_replace_dict(self):
        '''
        経験を記号に置き換えるための辞書を作成
        ex. 「少し飲む」→「少し」，「飲む」
        すべての語がwindowサイズ内にあれば記号に置き換える

        {
            'experience_replace_number_0': ['少し', '飲む'],
            'experience_replace_number_1': ['女性', '飲む']
            'experience_replace_number_2': ['一', '人', '飲む']
            ...
        }
        '''
        self.replace_dict = {} # initialize
        mt = MeCab.Tagger("-Ochasen")
        index = 0
        for experience in self.experiences.experiences:
            res = mt.parseToNode(experience.modifier + experience.verb)
            values = []
            while res:
                arr = res.feature.split(",")
                if arr[0] == '名詞' or arr[0] == '動詞' or arr[0] == '副詞' or arr[0] == '形容詞':
                    if arr[6] == '*':
                        values.append(res.surface)
                    else:
                        values.append(arr[6])
                res = res.next
            if len(values) == 1:
                continue
            key = 'experience_replace_number_' + str(index)
            self.replace_dict[key] = values
            index += 1

    def calc_words_weight(self):
        '''
        文書ごとに単語の重みを計算
        '''
        all_words_frequencies_dictionary = {}
        document_frequencies_dictionary = {}

        for document in self.documents:
            words_frequencies_dictionary = {}
            for word in document.words:
                if word not in all_words_frequencies_dictionary:
                    all_words_frequencies_dictionary[word] = 1
                else:
                    all_words_frequencies_dictionary[word] += 1

                if word not in words_frequencies_dictionary:
                    words_frequencies_dictionary[word] = 1

                    # dfの計算
                    if word not in document_frequencies_dictionary:
                        document_frequencies_dictionary[word] = 1
                    else:
                        document_frequencies_dictionary[word] += 1
                else:
                    words_frequencies_dictionary[word] += 1
            document.words_frequencies_dictionary = words_frequencies_dictionary
        self.all_words_frequencies_dictionary = all_words_frequencies_dictionary

        self.all_documents_weight = {}
        document_count = len(self.documents)
        for word, freq in all_words_frequencies_dictionary.items():
            df = document_frequencies_dictionary[word]
            idf = np.log(document_count/df) + 1
            for document in self.documents:
                tf = document.words_frequencies_dictionary[word] if  word in document.words_frequencies_dictionary else 0
                tfidf = tf * idf
                if document.document_id not in self.all_documents_weight:
                    self.all_documents_weight[document.document_id] = {word: tfidf}
                else:
                    self.all_documents_weight[document.document_id][word] = tfidf

        # normalyze by max value
        for key, document_weight in self.all_documents_weight.items():
            self.all_documents_weight[key] = normalyze_dictionary_by_maximum(document_weight)

    def make_documents_for_each_experience(self):
        words = {}
        for exp, _ in self.replace_dict.items():
            words[exp] = []
            for document in self.documents:
                if exp in document.words:
                    words[exp].extend(document.words)
        print(words)


    def write_documents(self, output_filename):
        '''
        self.documentsをテキストファイルに書き出す
        一文書（document）を一行に改行区切り
        Args:
            output_filename: str
        '''
        f = open(output_filename, 'w')
        for document in self.documents:
            text = ''
            for i in range(len(document.words)):
                text += document.words[i]
                if i == len(document.words) - 1:
                    text += '\n'
                else:
                    text += ' '
            f.write(text)
        f.close()

    def append(self, another_document):
        '''
        append a Document to the Documents

        Args:
            another_document: Document
        Returns:
            None
        '''
        if self.has_id(another_document.document_id):
            print('erorr: duplicate id: ' + str(another_document.document_id))
        else:
            self.documents.append(another_document)

    def extend(self, another_documents):
        '''
        extend the Documents by another Documents

        Args:
            another_documents: Documents
        Returns:
            None
        '''
        for another_document in another_documents.documents:
            if self.has_id(another_document.document_id):
                print('erorr: duplicate id: ' + str(another_document.document_id))
                return
        self.documents.extend(another_documents.documents)

    def has_id(self, document_id):
        return document_id in [doc.document_id for doc in self.documents]
    #
    # def get_around_experience(self, mod):
    #     results = []
    #     for word, frequent in sorted(self.words_around_experiences[mod].items(), key = lambda x: x[1], reverse=True):
    #         results.append([word, frequent])
    #
    #     return results

if __name__ == '__main__':
    # doc = Document()
    # doc.read_action_list('./act-drink.txt')
    # doc.read_document('./docs/tabelog/drink/reviews_by_normal_query_all_divided.txt')
    # doc.replace_actions('飲む', 5)
    # doc.write_document('./docs/tabelog/drink/replace_5.txt')
    # exit()
    #
    # doc = Document()
    # doc.read_action_list('./act-drink.txt')
    # doc.read_document('./docs/tabelog/drink/replace_cut_15.txt')
    # doc.get_words_around_actions(15)
    # # print(len(doc.words_around_actions))
    # print('done')
    # for query in sys.stdin:
    #     action = query.replace('\n', '')
    #     doc.show_words_around_action(action)
    # exit()

    # 周辺語を書き込む
    doc = Document()
    doc.read_action_list('../act-geo-matrix/actions/action_飲む_extended.txt')
    doc.read_document('../act-geo-matrix/reviews/search_test/all_bodies_replaced_100.txt')
    doc.get_words_around_actions(15)
    for action in doc.action_list:
        filename = './result/tabelog/drink_extended/' + action + '_around.txt'
        result = doc.get_around_action(action)
        f_w = open(filename, 'w')
        for r in result:
            line = r[0] + ':' + str(r[1]) + '\n'
            f_w.write(line)
        f_w.close()
    exit()
    print(sorted(doc.words_around_actions['ちょっと'].items(), key = lambda x: x[1]))
    exit()
    print('\n')
    print(doc.around_actions_indexes)

    # print(doc.around_words_indexes)

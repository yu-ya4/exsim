# -*-coding: utf-8 -*-

import MeCab
import sys

class Document():
    def __init__(self):
        self.document = []
        self.around_actions = {}
        self.around_actions_indexes = {}
        self.action_list = []
        self.replace_flg = 0

    def read_texts(self, filename):
        '''
        Args:
            filename: str
                分かち書きされた文書
        '''
        f = open(filename, 'r')
        for line in f:
            line = line.replace('\n', '')
            sentence = line.split(' ')
            self.document.append(sentence)
        f.close()

    def read_action_list(self, filename):
        '''
        Args:
            filename: str
                行動のリスト(一行につき一行動)
        '''
        self.action_list = []
        f = open(filename, 'r')
        for line in f:
            action = line.replace('\n', '')
            action = action.replace('"', '')
            self.action_list.append(action)
        f.close()

    def get_around_actions(self, window=5):
        '''
        リスト中の行動の周辺語を得る
            ex.) self.around_actions['ゆっくり飲む'] = {'バー': 10, ...}

        Args:
            window: int
                周辺語をとるサイズ
        '''
        # 初期化
        self.around_actions = {}
        self.around_actions_indexes = {}

        if not self.replace_flg:
            for action in self.action_list:
                around_action, around_actions_index = self.get_around_words(action, window)
                self.around_actions[action] = around_action
                self.around_actions_indexes[action] = around_actions_index
        else:
            i = 0
            for action in self.action_list:
                action_symbol = 'drink_replace_number_' + str(i)
                around_action, around_actions_index = self.get_around_words(action_symbol, window)
                self.around_actions[action] = around_action
                self.around_actions_indexes[action] = around_actions_index


    def get_around_words(self, target, window=5):
        '''
        対象語の周辺語を取得
        Args:
            target: str
                対象とする語
            window: int
                周辺語をとるサイズ
        Returns:
            around_words: Dictionary<str, int>
                周辺語をkey，出現頻度をvalueとした辞書
            around_words_indexes: Dictionary<str, List<int>>
                文書番号とターゲーットインデックスをkey，周辺語のリストのリストをvalueとした辞書
                {(文書番号:ターゲットインデックス): [around_words_index]}
        '''
        around_words = {}
        around_words_indexes = {}
        # 文章番号
        sen_i = 0
        for sentence in self.document:
            # 文章中の対象語のインデックスを取得
            target_indexes = [i for i, w in enumerate(sentence) if w == target]

            # 文章中に対象語があれば周辺語を取得
            if target_indexes:
                length = len(sentence)

                for i in target_indexes:
                    around_words_index = []
                    j = i + 1
                    while 1:
                        # 対象語よりウィンドウサイズ以内の語のインデックスを取得
                        # 文章の終わりに気をつける
                        if j >= length or j == i + window + 1:
                            break
                        around_words_index.append(j)
                        j += 1

                    j = i - 1
                    while 1:
                        # 文章の始まりに気をつける
                        if j < 0 or j == i - window - 1:
                            break
                        around_words_index.append(j)
                        j -= 1

                    for index in around_words_index:
                        # 周辺語の出現頻度を値とした辞書を作成
                        word = sentence[index]
                        if word in around_words:
                            around_words[word] += 1
                        else:
                            around_words[word] = 1

                    # 文章番号とターゲットインデックスをキーに，文章ごとの対象語の周辺語のインデックスを値とした辞書を作成
                    key = str(sen_i) + ':' + str(i)
                    around_words_indexes[key] = around_words_index
            sen_i += 1

        return around_words, around_words_indexes

    def show_around_action(self, action):
        '''
        特定の行動名の周辺語を出現頻度順に表示させる
        Args:
            action: 行動名
        '''
        print(sorted(self.around_actions[action].items(), key = lambda x: x[1]))

    def replace_actions_symbols(self, window=5):
        replace_dict = self.make_replace_dict()
        # 置換するターゲットを記憶する
        replace_target = {}
        # self.document = [['天気', 'が', '良い', 'ので', 'ちょっと', '出かけて', '飲む', 'こと', 'する'],
                            # ['さあ', '親', 'と', 'ちょっと', '飲む']]

        # 一時的に除外
        del replace_dict['drink_replace_number_18']
        del replace_dict['drink_replace_number_23']
        del replace_dict['drink_replace_number_30']
        del replace_dict['drink_replace_number_37']
        del replace_dict['drink_replace_number_42']

        around_words, around_words_indexes = self.get_around_words('飲む', window)
        for key, around_words_index in around_words_indexes.items():
            sen_i, target_id = map(int, key.split(':'))
            for i in around_words_index:
                for action_symbol, keyword in replace_dict.items():
                    if self.document[sen_i][i] == keyword[0]:
                        self.document[sen_i][i] = action_symbol
                        if action_symbol in replace_target:
                            replace_target[action_symbol].append([sen_i, target_id])
                        else:
                            replace_target[action_symbol] = [[sen_i, target_id]]

        for action_symbol, target_id in replace_target.items():
            for target in target_id:
                s_i, t_i = int(target[0]), int(target[1])
                if self.document[s_i][t_i] == '飲む':
                    self.document[s_i].pop(t_i)

                self.document[s_i].insert(t_i, action_symbol)

        self.replace_flg = 1

    def make_replace_dict(self):
        replace_dict = {}
        mt = MeCab.Tagger("-Ochasen")
        index = 0
        for action in self.action_list:
            res = mt.parseToNode(action)
            values = []
            while res:
                arr = res.feature.split(",")
                # print(arr)
                # とりあえず「飲む」専用
                if arr[0] == '動詞' and arr[6] == '飲む':
                    res = res.next
                    continue
                if arr[0] == '名詞' or arr[0] == '動詞' or arr[0] == '副詞' or arr[0] == '形容詞':
                    if arr[6] == '*':
                        values.append(res.surface)
                    else:
                        values.append(arr[6])
                res = res.next
            key = 'drink_replace_number_' + str(index)
            replace_dict[key] = values
            index += 1

        return replace_dict

    def write_document(self, filepath):
        f = open(filepath, 'w')
        for sentence in self.document:
            text = ''
            for word in sentence:
                text += word
                text += ' '
            text += '\n'
            f.write(text)

        f.close()


if __name__ == '__main__':
    doc = Document()
    doc.read_action_list('./actions.txt')
    doc.read_texts('./docs/tabelog/1_1_tabe_data.txt')
    doc.replace_actions_symbols(15)
    # doc.write_document('./docs/tabelog/1_1_tabe_data_replace.txt')
    # print(doc.get_around_words('ちょっと飲む', 5))
    doc.get_around_actions(15)
    # print(doc.around_actions)
    for query in sys.stdin:
        action = query.replace('\n', '')
        doc.show_around_action(action)
    exit()
    print(sorted(doc.around_actions['ちょっと飲む'].items(), key = lambda x: x[1]))
    exit()
    print('\n')
    print(doc.around_actions_indexes)

    # print(doc.around_words_indexes)

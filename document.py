# -*-coding: utf-8 -*-

import MeCab
import sys

class Document():
    def __init__(self):
        self.document = []
        self.words_around_actions = {}
        self.indexes_around_actions = {}
        self.action_list = []
        self.replace_flg = 0

    def read_document(self, filename):
        '''
        Args:
            filename: str
                分かち書きされた文書ファイル
        '''
        f = open(filename, 'r')
        for line in f:
            line = line.replace('\n', '')
            sentence = line.split(' ')
            self.document.append(sentence)
        f.close()

    def make_document(self, filename):
        '''
        Args:
            filename: str
                文書ファイル(分かち書きされていない)

        名詞，動詞，形容詞，副詞のみ
        原形で
        '''
        mt = MeCab.Tagger("-Ochasen")
        f = open(filename, 'r')
        for line in f:
            sentence = []
            line = line.replace('\n', '')
            res = mt.parseToNode(line)
            while res:
                arr = res.feature.split(",")
                if arr[0] == '名詞' or arr[0] == '動詞' or arr[0] == '副詞' or arr[0] == '形容詞':
                    if arr[6] == '*':
                        sentence.append(res.surface)
                    else:
                        sentence.append(arr[6])
                res = res.next
            # print(sentence)
            self.document.append(sentence)
        f.close()

    def read_action_list(self, filename):
        '''
        Args:
            filename: str
                一行につき一行動が記されたテキストファイル
        '''
        self.action_list = []
        f = open(filename, 'r')
        for line in f:
            action = line.replace('\n', '')
            self.action_list.append(action)
        f.close()

    def get_words_around_actions(self, window=5):
        '''
        リスト中の行動の周辺語を得る
            ex.) self.words_around_actions['ゆっくり飲む'] = {'バー': 10, ...}

        Args:
            window: int
                周辺語をとるサイズ
        '''
        # 初期化
        self.words_around_actions = {}
        self.indexes_around_actions = {}
        self.replace_flg = 1

        # 行動を記号で置き換えている時の対応
        if not self.replace_flg:
            for action in self.action_list:
                words, indexes = self.get_words_around_word(action, window)
                self.words_around_actions[action] = words
                self.indexes_around_actions[action] = indexes
        else:
            i = 0
            for action in self.action_list:
                action_symbol = 'action_replace_number_' + str(i)
                words, indexes = self.get_words_around_word(action_symbol, window)
                self.words_around_actions[action] = words
                self.indexes_around_actions[action] = indexes
                i+=1


    def get_words_around_word(self, target, window=5):
        '''
        対象語の周辺語を取得
        Args:
            target: str
                対象とする語
            window: int
                周辺語をとるサイズ
        Returns:
            words_around_word: Dictionary<str, int>
                周辺語をkey，出現頻度をvalueとした辞書
            indexes_around_word: Dictionary<str, List<int>>
                文書番号とターゲーットインデックスをkey，周辺語のリストのリストをvalueとした辞書
                {(文書番号:ターゲットインデックス): [indexes]}
        '''
        words_around_word = {}
        indexes_around_word = {}
        # 文章番号
        sen_i = 0
        for sentence in self.document:
            # 文章中の対象語のインデックスを取得
            target_indexes = [i for i, w in enumerate(sentence) if w == target]

            # 文章中に対象語があれば周辺語を取得
            if target_indexes:
                length = len(sentence)

                for i in target_indexes:
                    indexes = []
                    j = i + 1
                    while 1:
                        # 対象語よりウィンドウサイズ以内の語のインデックスを取得
                        # 文章の終わりに気をつける
                        if j >= length or j == i + window + 1:
                            break
                        indexes.append(j)
                        j += 1

                    j = i - 1
                    while 1:
                        # 文章の始まりに気をつける
                        if j < 0 or j == i - window - 1:
                            break
                        indexes.append(j)
                        j -= 1

                    for index in indexes:
                        # 周辺語の出現頻度を値とした辞書を作成
                        word = sentence[index]
                        if word in words_around_word:
                            words_around_word[word] += 1
                        else:
                            words_around_word[word] = 1

                    # 文章番号とターゲットインデックスをキーとし，
                    # 文章ごとの対象語に対する周辺語のインデックスを値とした辞書を作成
                    key = str(sen_i) + ':' + str(i)
                    indexes_around_word[key] = indexes
            sen_i += 1

        return words_around_word, indexes_around_word

    def show_words_around_action(self, action):
        '''
        特定の行動名の周辺語を出現頻度順に表示させる
        Args:
            action: 行動名
        '''
        print(sorted(self.words_around_actions[action].items(), key = lambda x: x[1]))

    def replace_actions(self, target_verb, window=5):
        '''
        Args:
            target: 周辺語を取得する対象語．'飲む'等の動詞を想定．
            window: windowサイズ
        '''
        replace_dict = self.make_replace_dict()
        # target_verbをキーワードから除く
        for symbol, keywords in replace_dict.items():
            if target_verb in keywords:
                keywords.remove(target_verb)

        # 語の原形を比較するため
        mt = MeCab.Tagger("-Ochasen")

        # 置換するターゲットを記憶する
        replace_targets = {}
        # self.document = [['天気', 'が', '良い', 'ので', '一', '人', 'で', 'ちょっと', '出かけて', '安く','飲む', 'こと', 'する'],
        #                     ['さあ', '親', 'と', 'ちょっと', '飲む', '。', '安い', 'し', '美味い']]

        words, indexes = self.get_words_around_word(target_verb, window)
        for key, index in indexes.items():
            sen_i, target_id = map(int, key.split(':'))
            for symbol, keywords in replace_dict.items():
                # keywordがすべて含まれていれば置換する
                keywords_in = True
                temp = []
                for keyword in keywords:
                    if not keywords_in:
                        break
                    for i in index:
                        res = mt.parseToNode(self.document[sen_i][i])
                        res = res.next
                        arr = res.feature.split(",")
                        if arr[6] == '*':
                            original_form = res.surface
                        else:
                            original_form = arr[6]
                        if original_form == keyword:
                            temp.append(i)
                            keywords_in = True
                            break
                        else:
                            keywords_in = False

                if keywords_in:
                    for i in temp:
                        # 記号に置換
                        self.document[sen_i][i] = symbol

                    if symbol in replace_targets:
                        replace_targets[symbol].append([sen_i, target_id])
                    else:
                        replace_targets[symbol] = [[sen_i, target_id]]
                else:
                    continue

        for symbol, targets in replace_targets.items():
            for target in targets:
                s_i, t_i = int(target[0]), int(target[1])

                if self.document[s_i][t_i] == target_verb:
                    # target消去
                    self.document[s_i].pop(t_i)

                self.document[s_i].insert(t_i, symbol)

        self.replace_flg = 1

    def make_replace_dict(self):
        '''
        行動を記号に置き換えるための辞書を作成
        ex. 「ちょっと飲む」→「ちょっと」，「飲む」
        すべての語がwindowサイズ内にあれば記号に置き換える
        '''
        replace_dict = {}
        mt = MeCab.Tagger("-Ochasen")
        index = 0
        for action in self.action_list:
            res = mt.parseToNode(action)
            values = []
            while res:
                arr = res.feature.split(",")
                if arr[0] == '名詞' or arr[0] == '動詞' or arr[0] == '副詞' or arr[0] == '形容詞':
                    if arr[6] == '*':
                        values.append(res.surface)
                    else:
                        values.append(arr[6])
                res = res.next
            key = 'action_replace_number_' + str(index)
            replace_dict[key] = values
            index += 1

        return replace_dict

    def write_document(self, filepath):
        '''
        self.documentをテキストファイルに書き出す
        '''
        f = open(filepath, 'w')
        for sentence in self.document:
            text = ''
            for i in range(len(sentence)):
                text += sentence[i]
                if i == len(sentence) - 1:
                    text += '\n'
                else:
                    text += ' '
            f.write(text)
        f.close()


    def get_around_action(self, action):
        results = []
        for word, frequent in sorted(self.words_around_actions[action].items(), key = lambda x: x[1], reverse=True):
            results.append([word, frequent])

        return results

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
    doc.read_action_list('./act-drink.txt')
    doc.read_document('./docs/tabelog/drink/replace_15.txt')
    doc.get_words_around_actions(15)
    for action in doc.action_list:
        filename = './result/tabelog/drink/replace_15_15/' + action + '_around.txt'
        result = doc.get_around_action(action)
        f_w = open(filename, 'w')
        for r in result:
            line = r[0] + ':' + str(r[1]) + '\n'
            f_w.write(line)
        f_w.close()
    exit()
    print(sorted(doc.around_actions['ちょっと飲む'].items(), key = lambda x: x[1]))
    exit()
    print('\n')
    print(doc.around_actions_indexes)

    # print(doc.around_words_indexes)

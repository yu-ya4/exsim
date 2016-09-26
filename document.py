# -*-coding: utf-8 -*-

class Document():
    def __init__(self):
        self.document = []
        self.around_words = {}
        self.around_words_indexes = {}
        self.action_list = []

    def read_texts(self, filename):
        f = open(filename)
        for line in f:
            line = line.replace('\n', '')
            sentence = line.split(' ')
            self.document.append(sentence)
        f.close()

    def read_action_list(self, filename):
        self.action_list = []
        f = open(filename, 'r')
        for line in f:
            action = line.replace('\n', '')
            action = action.replace('"', '')
            self.action_list.append(action)
        f.close()


    def get_around_words(self, target, window=5):
        self.around_words = {}
        self.around_words_indexes = {}
        sen_i = 0
        for sentence in self.document:
            target_indexes = [i for i, w in enumerate(sentence) if w == target]

            if target_indexes:
                around_words_index = []
                length = len(sentence)

                for i in target_indexes:
                    j = i + 1
                    while 1:
                        if j >= length or j == i + window + 1:
                            break
                        around_words_index.append(j)
                        j += 1

                    j = i - 1
                    while 1:
                        if j < 0 or j == i - window - 1:
                            break
                        around_words_index.append(j)
                        j -= 1

                for index in around_words_index:
                    word = sentence[index]
                    if word in self.around_words:
                        self.around_words[word] += 1
                    else:
                        self.around_words[word] = 1

                self.around_words_indexes[sen_i] = around_words_index
            sen_i += 1

        print(sorted(self.around_words.items(), key=lambda x: x[1]))

if __name__ == '__main__':
    doc = Document()
    doc.read_action_list('./actions.txt')
    doc.read_texts('./docs/data2.txt')
    doc.get_around_words('ちょっと飲む', 5)
    print(doc.around_words)
    # print(doc.around_words_indexes)

# -*-coding: utf-8 -*-

class Document():
    def __init__(self):
        self.document = []
        self.around_words = {}
        self.around_words_indexes = {}

    def read_texts(self, filename):
        f = open(filename)
        for line in f:
            line = line.replace('\n', '')
            sentence = line.split(' ')
            self.document.append(sentence)
        f.close()

    def get_around_words(self, target, window=5):
        self.around_words = {}
        self.around_words_indexes = {}
        sen_i = 0
        print(window)
        for sentence in self.document:

            target_indexes = [i for i, w in enumerate(sentence) if w == target]
            print(target_indexes)

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

if __name__ == '__main__':
    doc = Document()
    doc.read_texts('./data.txt')
    doc.get_around_words('です', 5)
    print(doc.around_words)
    print(doc.around_words_indexes)

# -*-coding: utf-8 -*-

class Document():
    def __init__(self):
        self.document = []

    def read_texts(self, filename):
        f = open(filename)
        for line in f:
            line = line.replace('\n', '')
            sentence = line.split(' ')
            self.document.append(sentence)
        f.close()

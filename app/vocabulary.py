import os
import json
from app.preprocessing  import Preprocessing

class Vocabulary():

    def __init__(self, model):
        self.preprocessing         =   Preprocessing(model)
        self.model                 =   model

    def read_config_vocabulary(self, keyword):
        config  =   {'vocab_size':0, 'data_count':0 }

        result  =   self.model.select_vocab_config(keyword)

        result  =  result if result else config

        return result

    def write_config_vocabulary(self, vocab_size, data_count, keyword):
        result  =   self.model.save_vocab_config(vocab_size, data_count, keyword)

    def write_vocabulary(self, list_word, list_idf, list_total, keyword):

        self.model.save_vocabulary(list_word, list_idf, list_total, keyword)

    def read_vocabulary(self, keyword):
        vocabulary      =   self.model.select_vocabulary(keyword)

        return vocabulary

    def create_vocabulary(self, data, keyword):
        vocabulary = self.read_vocabulary(keyword)

        for words in data:
            words_token   = self.preprocessing.tokennizing(words)
            for word in words_token:
                if word not in vocabulary:
                    vocabulary.append(word)

        vocabulary_size = len(vocabulary)
        data_count      = len(data)

        self.write_config_vocabulary(vocabulary_size, data_count, keyword)

        return vocabulary
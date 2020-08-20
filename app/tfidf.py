import os
import json
import math
import numpy as np
from app.vocabulary     import Vocabulary
from app.preprocessing  import Preprocessing

class TfIdf():

    def __init__(self, model):
        self.vocabulary         =   Vocabulary(model)
        self.proprecessing      =   Preprocessing(model)
        self.model              =   model

    def word_idf(self, document, keyword):
        total_document  = len(document)
        vocabulary      = self.vocabulary.create_vocabulary(document, keyword)
        idf             = []
        total           = []
        new_vocabulary  = []

        for feature in vocabulary:
            total_this_feature  = 0
            for data in document:
                list_word   =   self.proprecessing.tokennizing(data)
                if feature in list_word:
                    total_this_feature = total_this_feature + 1

            if total_this_feature < 2 or total_this_feature > 50 :
                pass
            else:
                idf.append(math.log(total_document/total_this_feature))
                total.append(total_this_feature)
                new_vocabulary.append(feature)

        self.write_vocabulary(new_vocabulary, idf, total, keyword)

    def tf(self, word1, data, length_sentences):
        freq_word = 0
        for word2 in data:
            if word1 == word2:
                freq_word = freq_word +1

        tf = float(freq_word/length_sentences)

        return tf


    def tf_idf(self, data, keyword, list_idf=False) :
        value               =  []
        list_idf            = self.read_idf(keyword) if not list_idf else list_idf
        list_word_text_now  =  []
        list_freq_word_now  =  []
        length_sentences    =  len(data)

        for word1 in data:
            if word1 in list_word_text_now:
                pass
            else:
                tf  =   self.tf(word1, data, length_sentences)
                list_word_text_now.append(word1)
                list_freq_word_now.append(tf)

        for features in list_idf:
            word    = features['word']
            idf     = features['idf']

            if word in list_word_text_now:
                freq_word_in_sentences = list_freq_word_now[list_word_text_now.index(word)]
                tfidf = float(freq_word_in_sentences) * float(idf)
                value.append(tfidf)
            else :
                value.append(0)

        return value

    def write_vocabulary(self, vocabulary, idf, total, keyword):
        self.vocabulary.write_vocabulary(vocabulary, idf, total, keyword)

    def read_idf(self, keyword):
        idf = self.model.select_idf(keyword)

        return idf
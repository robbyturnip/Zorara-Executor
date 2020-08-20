import re
import os
import json
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

class Preprocessing():

    def __init__(self, model):
        self.model_pre  =   model
        self.factory    =   StemmerFactory()
        self.stemmer    =   self.factory.create_stemmer()
        self.stopword   =   self.stopword_remover()
        self.kbba_fixer =   self.kbba()

    def case_folding(self, data):
        data      = data.lower()

        return data

    def regex_fix_word(self, match):
        word = match.group()
        word = word.split('_') if '_' in word else word.split()
        word = ''.join(word)
        word = ' ' + word + ' '

        return word

    def stopword_remover(self):
        stopwords     = self.model_pre.select_stopword_preprocessing()

        return stopwords

    def kbba(self):
        kbba_dictionary     = self.model_pre.select_kbba_preprocessing()

        return kbba_dictionary

    def remove_by_regex(self, data):
        data = re.sub('\s{1,}','  ', data)
        data = re.sub("\n"," ",data)
        data = re.sub("\t"," ",data)
        data = re.sub('&amp;',' ', data)
        data = re.sub("'|’",'', data)
        data = re.sub("http[s]?://(?:[a-z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+", " ", data)
        data = re.sub("@\w+"," ", data)
        data = re.sub("#\w+"," ", data)
        data = re.sub("\W"," ", data)
        data = re.sub('\s{2,}','-',data)
        data = re.sub("\s{1,1}","_", data)
        data = re.sub("(((_|-)([A-z]{,1}_)*)[A-z]_)\w",self.regex_fix_word, data)
        data = re.sub("_|-"," ", data)
        data = re.sub("\d"," ", data)
        data = re.sub("\s{2,}"," ", data)
        data = re.sub(r"((\s([A-z]{,1}\s)*)[A-z]\s)",self.regex_fix_word, data)
        data = re.sub(r"[ ](?=[A-z]{1,1}$)","", data)
        data = re.sub("((wk|kw){2,})(\w+|)", " ", data)
        data = re.sub("((gk|kg){2,})(\w+|)", " ", data)
        data = re.sub("((ha|ah){2,})(\w+|)", " ", data)
        data = re.sub("((ck|kc){2,})(\w+|)", " ", data)
        data = re.sub("((he|eh){2,})(\w+|)", " ", data)
        data = re.sub("((ho|oh){2,})(\w+|)", " ", data)
        data = re.sub("\s{2,}"," ", data)

        return data

    def remove_by_regex_2(self, data):
        data = re.sub(r"([a-z])\1+",lambda m: m.group(1), data)
        return data

    def fixing_kbba(self, data):

        data     = ' '.join(str(self.kbba_fixer.get(word, word)) for word in data).split()

        return data

    def remove_by_stopwords(self, data):
        data      = data.lower()
        data      = data.split()
        data      = self.fixing_kbba(data)
        data      = [word for word in data if word not in self.stopword]
        data      = " ".join(data)

        return data

    def stemming(self, data):

        return self.stemmer.stem(data)

    def cleansing(self, data):
        data_lower    = self.case_folding(data)
        data_stemming = self.stemming(data_lower)
        data_regex    = self.remove_by_regex(data_lower)
        data_stopword = self.remove_by_stopwords(data_regex)
        data_stemming = self.stemming(data_stopword)
        data_stemming = self.remove_by_stopwords(data_stemming)
        data_stemming = self.remove_by_regex_2(data_stemming)
        data_stemming = self.remove_by_stopwords(data_stemming)

        return data_lower, data_regex, data_stopword, data_stemming

    def tokennizing(self, inputs):
        inputs = inputs.split()

        return inputs
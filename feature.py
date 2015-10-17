#coding:utf-8
import os
import jieba
import jieba.posseg as pseg
import sys
import string
import codecs
import json
import sys
sys.path.append("../")
import jieba
#jieba.load_userdict("userdict.txt")
import jieba.posseg as pseg
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

class pretreatment():
    """预处理"""
    def __init__(self):
        pass
    def read_txt(self,txtPath,coding = 'utf-8'):
        import codecs
        f = codecs.open(txtPath,'r',coding).readlines()
        dataset = []
        for line in f:
            line = line.replace("\r\n","")
            line = line.replace("\n","")
            dataset.append(line)
        return dataset

    def cutWords(self, dataset):
        result = []
        for i in xrange(len(dataset)):
            temp = " ".join(jieba.cut(dataset[i]))
            result.append(temp)
        return result

class tfidf():
    def __init__():
        pass
    def tfidf(self, dataset, num):
        corpus = self.cutWords(dataset)
        vectorizer=CountVectorizer()#该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频
        transformer=TfidfTransformer()#该类会统计每个词语的tf-idf权值
        #print vectorizer.fit_transform(corpus)
        tfidf=transformer.fit_transform(vectorizer.fit_transform(corpus))#第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵
        #print tfidf
        word=vectorizer.get_feature_names()#获取词袋模型中的所有词语
        weight=tfidf.toarray()#将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重
        for i in xrange(len(weight[0])):
            word[i] = (word[i],sum(weight[:,i])) 
        word = sorted(word,key=lambda word_tuple:word_tuple[1],reverse=1)[0:num]
        word = [i[0] for i in word]
        return word


class Methods(tfidf,pretreatment):
    pass

class DataAnalysis(pretreatment, Methods):
    pass



if __name__=='__main__':
    data = DataAnalysis().read_txt('E:\\dev\\AboutFeature\\data\\data1.txt')
    word = DataAnalysis().tfidf(data,20)
    print word


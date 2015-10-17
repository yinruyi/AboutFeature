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

    def count(self, dataset):
        #计数
        count = {}
        for i in dataset:
            if i in count:
                count[i] += 1
            else:
                count[i] =1
        return count

    def filter_tuple(self, dataset):
        #对元组进行过滤
        filter_words = [u",",u".",u"，",u"。",u")",u"(",u"（",u"）"]
        result = []
        for i in dataset:
            if i[0] not in filter_words:
                result.append(i)
        return result


class tf():
    def __init__():
        pass
    def tf(self, dataset, num):
        dataset = self.cutWords(dataset)
        temp,word= [],[]
        for i in dataset:
            temp.extend(i.split())
        dataset = self.count(temp)
        for k,v in dataset.items():
            word.append((k,v))
        word = self.filter_tuple(word)
        word = sorted(word,key=lambda word_tuple:word_tuple[1],reverse=1)[0:num]
        word = [i[0] for i in word]
        #print word
        return word

class df():
    def __init__():
        pass
    def df(self, dataset, num):
        dataset = self.cutWords(dataset)
        temp,word= [],[]
        for i in dataset:
            temp.extend(list(set(i.split())))
        dataset = self.count(temp)
        for k,v in dataset.items():
            word.append((k,v))
        word = self.filter_tuple(word)
        word = sorted(word,key=lambda word_tuple:word_tuple[1],reverse=1)[0:num]
        word = [i[0] for i in word]
        #print word
        return word

class idf():
    def __init__(self):
        pass
    def idf(self, dataset, num):
        pass

        

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


class mi():
    def __init__():
        pass
    def mi(self, dataset, num):
        pass


        
class Methods(tfidf, tf, df, mi, idf):
    pass

class DataAnalysis(pretreatment, Methods):
    pass



if __name__=='__main__':
    data = DataAnalysis().read_txt('E:\\dev\\AboutFeature\\data\\data1.txt')
#tfidf
    #word = DataAnalysis().tfidf(data,20)
#tf
    #word = DataAnalysis().tf(data,20)
#df
    #word = DataAnalysis().df(data,20)
#idf
    word = DataAnalysis().idf(data,20)
    print word

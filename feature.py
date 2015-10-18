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
import math
from gensim import corpora, models, similarities

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
        #分词
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
        dataset = self.cutWords(dataset)
        data_length = len(dataset)
        print data_length
        temp,word= [],[]
        for i in dataset:
            temp.extend(list(set(i.split())))
        dataset = self.count(temp)
        for k,v in dataset.items():
            word.append((k,v))
        word = self.filter_tuple(word)
        temp = []
        for i in word:
            temp.append((i[0],math.log(1.0*data_length/i[1])))
        word = temp
        word = sorted(word,key=lambda word_tuple:word_tuple[1],reverse=1)[0:num]
        return word     

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

class pmi():
    def __init__():
        pass
    def pmi(self, dataset, threshold):
        dataset = self.cutWords(dataset)
        single,double= [],[]
        for i in xrange(len(dataset)):
            temp = dataset[i].split()
            #print temp
            for j in xrange(len(temp)):
                single.append(temp[j])
            if len(temp) > 1:
                for j in xrange(len(temp)-1):
                    double.append((temp[j],temp[j+1]))
        #print len(single),len(double)
        len_single, len_double = len(single) ,len(double)
        single = self.count(single)
        double = self.count(double)
        word = []#结果[((a,b),pmi)]
        for k,v in double.items():
            pxy = 1.0*v/len_double
            px,py = 1.0*single[k[0]]/len_single,1.0*single[k[1]]/len_single
            pmi = math.log(pxy/(px*py))
            if pmi >= threshold:
                word.append((k,pmi))
        #print word
        word = sorted(word,key=lambda word_tuple:word_tuple[1],reverse=1)
        #print word
        word = [i[0] for i in word]
        result = []
        for i in word:
            result.extend([i[0],i[1]])
        result = list(set(result))
        return result

class chi_square():
    def __init__():
        pass
    def chi_square(self, dataset, threshold):
        dataset = self.cutWords(dataset)
        single,double= [],[]
        for i in xrange(len(dataset)):
            temp = dataset[i].split()
            #print temp
            for j in xrange(len(temp)):
                single.append(temp[j])
            if len(temp) > 1:
                for j in xrange(len(temp)-1):
                    double.append((temp[j],temp[j+1]))
        chi_temp = {}#{(a,b):[a,b,c,d]}
        for i in double:
            if i not in chi_temp:
                a,b,c,d = 0,0,0,0
                for j in double:
                    if i[0] == j[0] and i[1] == j[1]:
                        a += 1
                    elif i[0] == j[0] and i[1] != j[1]:
                        b += 1
                    elif i[0] != j[0] and i[1] == j[1]:
                        c += 1
                    elif i[0] != j[0] and i[1] != j[1]:
                        d += 1
                chi_temp[i] = [a,b,c,d]
        word = []
        for k,v in chi_temp.items():
            chi_square_temp = 1.0*(v[0]*v[3]-v[1]*v[2])**2/((v[0]+v[1])*(v[2]+v[3]))
            word.append((k,chi_square_temp,v[0]))
        word = sorted(word,key=lambda word_tuple:word_tuple[1],reverse=1)[0:20]
        #print word
        word = [i[0] for i in word]
        return word

class lsi():
    def __init__():
        pass
    def lsi(self, dataset):
        documents = ["Shipment of gold damaged in a fire",
                    "Delivery of silver arrived in a silver truck",
                    "Shipment of gold arrived in a truck"]
        texts = [[word for word in document.lower().split()] for document in documents]
        print texts
        dictionary = corpora.Dictionary(texts)
        print dictionary
        print dictionary.token2id
        corpus = [dictionary.doc2bow(text) for text in texts]
        print corpus
        tfidf = models.TfidfModel(corpus)
        print tfidf
        corpus_tfidf = tfidf[corpus]
        print corpus_tfidf
        print tfidf.dfs
        print tfidf.idfs
        lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=2)
        print lsi.print_topics(2)
        corpus_lsi = lsi[corpus_tfidf]
        for doc in corpus_lsi:
            print doc
        lda = models.LdaModel(copurs_tfidf, id2word=dictionary, num_topics=2)
        print  lda.print_topics(2)
        index = similarities.MatrixSimilarity(lsi[corpus])
        print index
        
                      
class Methods(tfidf, tf, df, pmi, idf, chi_square, lsi):
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
    #word = DataAnalysis().idf(data,20)
#pmi
    #word = DataAnalysis().pmi(data,threshold=10)
#chi_square
    #word = DataAnalysis().chi_square(data,threshold=10)
    #print word
#lsi/lsa
    word = DataAnalysis().lsi(data)
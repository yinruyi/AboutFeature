#coding:utf-8
from string import punctuation
import re
import codecs
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

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

	def writeString(self,string,txtPath = 'out.txt'):
		#将String写入文件
		f = open(txtPath, "a+")
		line = f.write(string + '\n')
		f.close

class DataAnalysis(pretreatment):
	pass



if __name__=='__main__':
    data = DataAnalysis().read_txt('E:\\dev\\AboutFeature\\data\\MISQ.txt')
    #print data[1].lower()
    #print punctuation
    for i in xrange(len(data)):
    	for j in punctuation:
    		data[i] = (" "+j+" ").join(data[i].split(j))
    	data[i] = data[i].lower()
   	print data[0]
		#print data[i]
	#print data[1]
	string = "\n".join(data)
	print string[0:10]
	f = open("testa.txt","a")
	f.close()
	open("MISQ_lower.txt","w").write(string)
	#print string
	#import json
	#with open("MISQ_lower.txt", "w") as f:
		#json.dump(data, f)


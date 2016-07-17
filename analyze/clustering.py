# coding=utf-8  
import pymongo
import pandas as pd
import datetime
from dateutil.parser import parse

# set up
strFileUserDictStockSymbol = 'userDictStockSymbol.txt'

# retrieve data from database
client = pymongo.MongoClient()
db = client['stackoverflow']
collection = db['questions']
iterDoc = collection.find({
    "dtCrawled": {
        "$gt": datetime.datetime(2016, 6, 16)
        }
    })
listJSON = [doc for doc in iterDoc]
dfNews = pd.DataFrame(listJSON)

# cut text
import jieba
jieba.load_userdict(strFileUserDictStockSymbol)
def funCutRawTextToList(text):
    if text is not None:
        return jieba.lcut(text)

dfNews['title_cut'] = dfNews['title']
dfNews['title_cut'] = dfNews['title_cut'].apply(funCutRawTextToList)
dfNews['text_cut'] = dfNews['text']
dfNews['text_cut'] = dfNews['text_cut'].apply(funCutRawTextToList)

# rank the popularity of the stock symbols
listWords = dfNews['title_cut'].to_dict().values() + dfNews['text_cut'].to_dict().values()
dictWords = {}
for listOne in listWords:
    if listOne is not None:
        for word in listOne:
            if dictWords.has_key(word):
                dictWords[word] = dictWords[word] + 1
            else:
                dictWords[word] = 1

listStockName = pd.read_csv(strFileUserDictStockSymbol, header=None, encoding='utf-8')[0].to_dict().values()
dictWordsStock = {k: dictWords[k] for k in listStockName if dictWords.has_key(k)}
seriesWordsStock = pd.Series(dictWordsStock).sort_values()

# clustering of a given stock
import time          
import re          
import os  
import sys
import codecs
import shutil
import numpy as np
import matplotlib
import scipy
import matplotlib.pyplot as plt
from sklearn import feature_extraction  
from sklearn.feature_extraction.text import TfidfTransformer  
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import HashingVectorizer 

strStockName = u"信达地产"
#########################################################################
#                           第一步 计算TFIDF

#文档预料 空格连接
corpus = []

#读取预料 一行预料为一个文档
for listCut in dfNews['text_cut'].to_dict().values():
    if strStockName in listCut:
        corpus.append(' '.join(listCut))
#print corpus

#参考: http://blog.csdn.net/abcjennifer/article/details/23615947
#vectorizer = HashingVectorizer(n_features = 4000)


#将文本中的词语转换为词频矩阵 矩阵元素a[i][j] 表示j词在i类文本下的词频
vectorizer = CountVectorizer()

#该类会统计每个词语的tf-idf权值
transformer = TfidfTransformer()

#第一个fit_transform是计算tf-idf 第二个fit_transform是将文本转为词频矩阵
tfidf = transformer.fit_transform(vectorizer.fit_transform(corpus))

#获取词袋模型中的所有词语  
word = vectorizer.get_feature_names()


#将tf-idf矩阵抽取出来，元素w[i][j]表示j词在i类文本中的tf-idf权重
weight = tfidf.toarray()

#打印特征向量文本内容
print 'Features length: ' + str(len(word))
resName = "BHTfidf_Result.txt"
result = codecs.open(resName, 'w', 'utf-8')
for j in range(len(word)):
    result.write(word[j] + ' ')
result.write('\r\n\r\n')

#打印每类文本的tf-idf词语权重，第一个for遍历所有文本，第二个for便利某一类文本下的词语权重  
for i in range(len(weight)):
    #print u"-------这里输出第", i, u"类文本的词语tf-idf权重------"  
    for j in range(len(word)):
        #print weight[i][j],
        result.write(str(weight[i][j]) + ' ')
    result.write('\r\n\r\n')
result.close()

########################################################################
#                               第二步 聚类Kmeans
print 'Start Kmeans:'
from sklearn.cluster import KMeans
clf = KMeans(n_clusters=4)   #景区 动物 人物 国家
s = clf.fit(weight)
print s

'''
print 'Start MiniBatchKmeans:'
from sklearn.cluster import MiniBatchKMeans
clf = MiniBatchKMeans(n_clusters=20)
s = clf.fit(weight)
print s
'''

#中心点
print(clf.cluster_centers_)

#每个样本所属的簇
label = []               #存储1000个类标 4个类
print(clf.labels_)
i = 1
while i <= len(clf.labels_):
    print i, clf.labels_[i-1]
    label.append(clf.labels_[i-1])
    i = i + 1

#用来评估簇的个数是否合适，距离越小说明簇分的越好，选取临界点的簇个数  958.137281791
print(clf.inertia_)

########################################################################
#                               第三步 图形输出 降维
from sklearn.decomposition import PCA
pca = PCA(n_components=2)             #输出两维
newData = pca.fit_transform(weight)   #载入N维
print newData


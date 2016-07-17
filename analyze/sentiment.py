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

import snownlp 
from snownlp import SnowNLP

dfNews['title_cut'] = dfNews['title']
dfNews['title_cut'] = dfNews['title_cut'].apply(funCutRawTextToList)
dfNews['text_cut'] = dfNews['text']
dfNews['text_cut'] = dfNews['text_cut'].apply(funCutRawTextToList)
#dfNews['text_SnowNLP'] = dfNews['text'].apply(lambda x: SnowNLP(x))

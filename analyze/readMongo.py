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


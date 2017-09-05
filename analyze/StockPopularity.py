import pymongo
import pandas as pd
import datetime
from dateutil.parser import parse

# set up
strFileUserDictStockSymbol = 'userDictStockSymbol.txt'
listStockName = pd.read_csv(strFileUserDictStockSymbol, header=None, encoding='utf-8')[0].to_dict().values()

# retrieve data from database
client = pymongo.MongoClient()
db = client['stackoverflow']
collection = db['questions']
iterDoc = collection.find({
    "dtCrawled": {
        "$gt": datetime.datetime(2017, 1, 1)
        },
    "source": "Sina",
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
dtLatest = dfNews['dtCreated'].max() + datetime.timedelta(1, 0)
dtLatest = datetime.datetime.combine(dtLatest, datetime.time(0, 0))
listDate = pd.date_range(dtLatest-datetime.timedelta(3), dtLatest).tolist()

strDate = 'dtCreated'
listSeriesStock = []
listSeriesStockTitle = []
for nDate, dt in enumerate(listDate[0:]):
    dtPrev = listDate[nDate-1]
    dfNewsOneDay = dfNews[(dfNews[strDate]>=dtPrev)&(dfNews[strDate]<dt)]
    dictWords = {}
    dictWordsListTitle = {}
    for ix, row in dfNewsOneDay.iterrows():
        listOne = row['title_cut'] + row['text_cut']
        if listOne is not None:
            for word in listOne:
                if word not in listStockName:
                    continue

                if dictWords.has_key(word):
                    dictWords[word] = dictWords[word] + 1
                    dictWordsListTitle[word].append(row['title'])
                else:
                    dictWords[word] = 1
                    dictWordsListTitle[word] = [row['title']]

    seriesWordsStock = pd.Series(dictWords).sort_values()
    seriesWordsStock.name = dt
    listSeriesStock.append(seriesWordsStock)
    
    seriesStockTitle = pd.Series(dictWordsListTitle).sort_values()
    seriesStockTitle.name = dt
    listSeriesStockTitle.append(seriesStockTitle)

dfStockCount = pd.concat(listSeriesStock, axis=1)
dfStockTitle = pd.concat(listSeriesStockTitle, axis=1)



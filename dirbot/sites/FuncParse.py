import re
#import jieba
def readStockSymbols():
    dictStockSymbols = {}
    fh = open('StockSymbols.csv', 'r')
    lines = fh.readlines()
    for line in lines:
        line.strip()
        words = line.split(',')
        code = words[0]
        abbr = words[1]
        abbr = abbr.replace(' ', '')
        abbr = abbr.replace('\xa3\xc1', '')
        name = words[2]
        dictStockSymbols[abbr.decode('gbk')] = code
    fh.close()
    return dictStockSymbols

def readKeyWordsPositive():
    fileAddress = 'KeyWordsPositive.csv'
    listKeyWords = readKeyWords(fileAddress)
    
    dictStockSymbols = readStockSymbols()
    listKeyWords = listKeyWords + dictStockSymbols.keys()
    return listKeyWords

def readKeyWordsNegative():
    fileAddress = 'KeyWordsNegative.csv'
    listKeyWords = readKeyWords(fileAddress)
    return listKeyWords

def readKeyWords(fileAddress):
    listKeyWords = []
    fh = open(fileAddress, 'r')
    lines = fh.readlines()
    for line in lines:
        line.strip()
        words = line.split(',')
        for word in words:
            if word is not '':
                listKeyWords.append(word.decode('gbk'))
    fh.close()
    return listKeyWords

def filterByKeyWords(text, listStocksSymbols):
    listRet = []
    for word in listStocksSymbols:
        if text.find(word) >= 0:
            listRet.append(word)
    return listRet

def checkTitle(title, listKeyWordsPositive, listKeyWordsNegative):
    '''
    for word in listKeyWordsPositive:
        if title.find(word) > 0:
            return True
    '''

    #pattern = re.compile(u".*?(\d+)[\u4e00-\u9fa5](\d+)[\u4e00-\u9fa5].*?")
    pattern = re.compile(u".*?(\d+)\D*?(\d+)\D*?.*?")
    if pattern.match(title) is not None:
        return False
    for word in listKeyWordsNegative:
        if title.find(word) > 0:
            return False

    return True

def compare(keyword, textToBeCompared):
    numMatched = 0
    for n in range(0, len(keyword)):
        if textToBeCompared.find(keyword[n]) > 0:
            numMatched = numMatched + 1

    if len(keyword) == 0:
        ret = 0
    else:
        ret = float(numMatched) / len(keyword)

    return ret

'''
jieba.load_userdict('./data/userdict.txt')

#fh = open('./data/shierwu.txt')
fh = open('./data/yidaiyilu.txt')
text = fh.readlines()
text = ' '.join(text)
text = text.decode('gbk')
fh.close()

default_mode = jieba.cut(text)
full_mode = jieba.cut(text, cut_all=True)
search_mode = jieba.cut_for_search(text)

setWords = set(default_mode)
setWordsFull = set(full_mode)
setWordsSearch = set(search_mode)

fh = open('./data/temp.txt', 'w')
for word in setWordsFull:
    fh.write(word.encode('gbk') + '\n')
fh.close()
'''

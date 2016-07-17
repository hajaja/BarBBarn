# -*- coding: utf-8 -*-
import wx
import wx.lib.agw.hyperlink as wxHyperLink
import wx.lib.buttons as buttons
import datetime
import FuncCrawl
import FuncParse
import threading
import FuncDB
import FuncBaidu
import time
import threading
import sys
import pdb
reload(sys)
sys.setdefaultencoding('utf-8')

hostName = "176.1.1.154"
dbName = "pub"
userName = "ye"
password = "19860417"
tbNameNews = "tbNewsHistory"
tbNameFulltext = "tbFulltextHistory"

listKeyWordsPositive = FuncParse.readKeyWordsPositive()
listKeyWordsNegative = FuncParse.readKeyWordsNegative()
linkAddressPrefix = 'http://news.cnstock.com/bwsd/'
for n in range(5, 114):
    print 'page:%s'%(n)
    linkAddress = linkAddressPrefix + str(n)

    nRepeated = 0
    while True:
        dictNews = FuncCrawl.retrieveNewsCNStockLatestHistory(linkAddress)
        nRepeated = nRepeated + 1
        if dictNews is not None:
            break
        if nRepeated > 2:
            break

    dictThreadParsePage = {}
    for title in dictNews:
        threadParsePage = FuncCrawl.ClassThreadParsePage(
                title,
                FuncCrawl.parsePageStockLatest,
                {
                    'link': dictNews[title]['link'],
                    'listKeyWordsPositive': listKeyWordsPositive
                }
                )
        dictThreadParsePage[threadParsePage] = title
        threadParsePage.setDaemon(True)
        threadParsePage.start()

    for threadParsePage in dictThreadParsePage:
        threadParsePage.join()

    print 'original link join completed'

    dictThreadParsePageViaBaidu = {}
    for threadParsePage in dictThreadParsePage:
        if len(threadParsePage.dictRet) != 0:
            title = dictThreadParsePage[threadParsePage]
            dictNews[title]['keywords'] = threadParsePage.dictRet['listKeyWordsCollected']
            dictNews[title]['datetime'] = threadParsePage.dictRet['datetime']
            dictNews[title]['fulltext'] = threadParsePage.dictRet['fulltext']
        else:
            # if the news is not available on news.cnstock.com
            try:
                dictOneFromBaidu = FuncBaidu.getNewsBasic(title)
            except:
                dictOneFromBaidu = None
            if dictOneFromBaidu is not None:
                dictNews[title] = dictOneFromBaidu
                dictNews[title]['source'] = '上证快讯'.decode('gbk')
            else:
                continue
            if dictNews[title]['link'].find('cnstock') > 0:
                threadParsePageViaBaidu = FuncCrawl.ClassThreadParsePage(
                        title,
                        FuncCrawl.parsePageStockLatest,
                        {
                            'link': dictNews[title]['link'],
                            'listKeyWordsPositive': listKeyWordsPositive
                        }
                        )
                dictThreadParsePageViaBaidu[threadParsePageViaBaidu] = title
                threadParsePageViaBaidu.setDaemon(True)
                threadParsePageViaBaidu.start()
    
    for threadParsePageViaBaidu in dictThreadParsePageViaBaidu:
        threadParsePageViaBaidu.join()

    print 'baidu link join completed'
    
    for threadParsePageViaBaidu in dictThreadParsePageViaBaidu:
        if len(threadParsePageViaBaidu.dictRet) != 0:
            title = dictThreadParsePageViaBaidu[threadParsePageViaBaidu]
            dictNews[title]['keywords'] = threadParsePageViaBaidu.dictRet['listKeyWordsCollected']
            dictNews[title]['datetime'] = threadParsePageViaBaidu.dictRet['datetime']
            dictNews[title]['fulltext'] = threadParsePageViaBaidu.dictRet['fulltext']
            dictNews[title]['source'] = '上证快讯'.decode('gbk')
    
    conn = FuncDB.connect(hostName, dbName, userName, password)
    FuncDB.insertWithListDictOne(conn, dictNews.values(), tbNameNews)
    conn.commit()
    conn.close()
    time.sleep(10)

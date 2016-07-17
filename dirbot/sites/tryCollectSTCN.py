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
import pdb
from dateutil.parser import parse

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

hostName = "176.1.1.154"
dbName = "pub"
userName = "ye"
password = "19860417"
'''
hostName = "localhost"
dbName = "db1"
userName = "csdong"
password = "19860417"
'''
tbNameNews = "tbNewsHistory"
tbNameFulltext = "tbFulltextHistory"

listKeyWordsPositive = FuncParse.readKeyWordsPositive()
listKeyWordsNegative = FuncParse.readKeyWordsNegative()

datetimeStart = datetime.datetime(2012,1,1)
#datetimeEnd = datetime.datetime.now()
datetimeEnd = datetime.datetime(2015,9,20)
datetimeThis = datetimeStart

source = 'www.cnstock.com'

while datetimeThis < datetimeEnd:
    #listDictOne = FuncBaidu.getNewsAdvanced('', datetimeThis - datetime.timedelta(1), datetimeThis, 'finance.sina.com.cn')
    listDictOne = FuncBaidu.getNewsAdvanced('', datetimeThis - datetime.timedelta(1), datetimeThis, source)
    numConnection = 0
    while numConnection < 5:
        try:
            conn = FuncDB.connect(hostName, dbName, userName, password)
            FuncDB.insertWithListDictOne(conn, listDictOne, tbNameNews)
            conn.commit()
            conn.close()
            time.sleep(1)
            break
        except:
            numConnection = numConnection + 1
            time.sleep(1)
    datetimeThis = datetimeThis + datetime.timedelta(1)

#aa = FuncBaidu.getNewsAdvanced('', datetimeStart, datetimeEnd, 'finance.sina.com.cn')

'''
threadParsePage = ClassThreadParsePage(
        'title for test',
        FuncParse.parsePageSina,
        {
            'link': 'http://finance.sina.com.cn/stock/newstock/zxdt/20140102/075917820155.shtml',
            'listKeyWordsPositive': listKeyWordsPositive
            }
        )
threadParsePage.start()

aa = FuncCrawl.parsePageSina(
        {
            'link': 'http://finance.sina.com.cn/roll/20140102/070817819582.shtml',
            'listKeyWordsPositive': listKeyWordsPositive
            }
        )
'''



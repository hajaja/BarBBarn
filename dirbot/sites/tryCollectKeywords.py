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

listKeyWords = ['宋城演艺', '国旅联合', '北部湾旅', '众信旅游', '桂林旅游', '丽江旅游', '峨眉山A', '黄山A', '云南旅游', '大连圣亚']

datetimeStart = datetime.datetime(2015,8,27)
datetimeEnd = datetime.datetime(2015,9,27)

#source = 'finance.ifeng.com'
source = None

for keyword in listKeyWords:
    print keyword
    listDictOne = FuncBaidu.getNewsAdvanced(keyword, datetimeStart, datetimeEnd, source)
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


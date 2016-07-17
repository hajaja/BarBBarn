import FuncCrawl
import FuncDB
from dateutil.parser import parse
import time

import re

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

n = 1

while True:
    site = 'http://znjs.most.gov.cn/wasdemo/search?page=%d&channelid=18220&prepage=20'%n
    n = n + 1
    soup = FuncCrawl.getSoupOfLink(site, 'utf-8', 'utf-8')
    # find interesting titles
    sourceName = '¿Æ¼¼²¿'.decode('gbk')
    dictNewsSelected = {}
    divSelected = soup.findAll('a')
    for taga in divSelected:
        if len(taga.text) < 8:
            continue
        textDate = re.compile('.*?(\d+\.\d+\.\d+).*?').match(taga.parent.text).groups()[0]
        dtFromPage = parse(textDate)
        FuncCrawl.fillDictNewsWithA(dictNewsSelected, taga, sourceName, dtFromPage)
    listDictOne = dictNewsSelected.values()
    print len(listDictOne)
    conn = FuncDB.connect(hostName, dbName, userName, password)
    FuncDB.insertWithListDictOne(conn, listDictOne, tbNameNews)
    conn.commit()
    conn.close()
    time.sleep(1)

    print site

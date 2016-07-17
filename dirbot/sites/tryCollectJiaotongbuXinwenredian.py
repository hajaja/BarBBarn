import FuncCrawl
import FuncDB
from dateutil.parser import parse
import time
import datetime

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

urlPrefix = 'http://www.moc.gov.cn/zhuzhan/jiaotongxinwen/xinwenredian/'
    
dt1 = datetime.datetime(2014,12,1)
while True:
    if dt1.month == 1:
        dt1 = datetime.datetime(dt1.year - 1, 12, 1)
    else:
        dt1 = datetime.datetime(dt1.year, dt1.month-1, 1)
    print dt1

    url = urlPrefix + dt1.strftime('%Y%m') + 'xinwen/index'
    site = url + '.html'
    n = 1
    
    while True:
        soup = FuncCrawl.getSoupOfLink(site, 'utf-8', 'utf-8')
        # find interesting titles
        sourceName = '½»Í¨²¿'.decode('gbk')
        dictNewsSelected = {}
        listTr = soup.findAll('tr')
        for tr in listTr:
            listTd = tr.findAll('td')
            if len(listTd) < 3:
                continue
            td = listTd[2]
            if td.get('width') != '91':
                continue
            textTime = td.text[1:-1]
            print textTime
            taga = tr.findAll('a')[0]
            dtFromPage = parse(textTime)
            FuncCrawl.fillDictNewsWithA(dictNewsSelected, taga, sourceName, dtFromPage)
        listDictOne = dictNewsSelected.values()
        print len(listDictOne)
        if len(listDictOne) == 0:
            break
        conn = FuncDB.connect(hostName, dbName, userName, password)
        FuncDB.insertWithListDictOne(conn, listDictOne, tbNameNews)
        conn.commit()
        conn.close()
        time.sleep(1)
    
        site = url + '_' + str(n) + '.html'
        n = n + 1
        print site

import FuncCrawl
import FuncDB
from dateutil.parser import parse
import time

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

#url = 'http://www.nea.gov.cn/2015v/policy/tz'
#url = 'http://www.nea.gov.cn/2015v/policy/zxwj'
#url = 'http://www.nea.gov.cn/2015v/policy/jd'
#url = 'http://www.nea.gov.cn/2015v/policy/qt'
url = 'http://www.nea.gov.cn/sjzz/ghs/index'
site = url + '.htm'
n = 1

while True:
    soup = FuncCrawl.getSoupOfLink(site, 'utf-8', 'utf-8')
    # find interesting titles
    sourceName = 'ÄÜÔ´¾Ö'.decode('gbk')
    dictNewsSelected = {}
    listLi = soup.findAll('li')
    for li in listLi:
        try:
            span = li.findAll('span')[0]
        except:
            print li
            continue

        taga = li.findAll('a')[0]
        dtFromPage = parse(span.text)
        FuncCrawl.fillDictNewsWithA(dictNewsSelected, taga, sourceName, dtFromPage)
    listDictOne = dictNewsSelected.values()
    print len(listDictOne)
    conn = FuncDB.connect(hostName, dbName, userName, password)
    FuncDB.insertWithListDictOne(conn, listDictOne, tbNameNews)
    conn.commit()
    conn.close()
    time.sleep(1)

    site = url + '_' + str(n) + '.htm'
    n = n + 1
    print site

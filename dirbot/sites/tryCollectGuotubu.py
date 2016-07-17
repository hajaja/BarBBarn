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

#url = 'http://www.mlr.gov.cn/zwgk/ghjh/index'
#url = 'http://news.mlr.gov.cn/xwdt/jrxw/index'
#url = 'http://www.mlr.gov.cn/zwgk/zytz/index'
#url = 'http://news.mlr.gov.cn/xwdt/tdxw/index'
url = 'http://news.mlr.gov.cn/xwdt/kyxw/index'
site = url + '.htm'
n = 1

while True:
    soup = FuncCrawl.getSoupOfLink(site, 'utf-8', 'utf-8')
    # find interesting titles
    sourceName = '¹úÍÁ²¿'.decode('gbk')
    dictNewsSelected = {}
    listTd = soup.findAll('td', {'class':'outlinebig'})
    for td in listTd:
        taga = td.findAll('a')[0]
        textTime = td.parent.findAll('td')[2].text
        dtFromPage = parse(textTime)
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

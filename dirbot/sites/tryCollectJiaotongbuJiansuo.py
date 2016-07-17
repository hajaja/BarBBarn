import FuncCrawl
import FuncDB
from dateutil.parser import parse
import time
import re
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

#url = 'http://www.moc.gov.cn/zfxxgk//249/list_4557'
url = 'http://wcm.mot.gov.cn:9000/govsearch/searPage.jsp?page='
site = url + '16' + '&pubwebsite=zfxxgk&indexPa=1&schn=249&sinfo=249&surl=zfxxgk/249/list_4557_14.htm&curpos=%E6%9C%BA%E6%9E%84%E5%88%86%E7%B1%BB'

n = 17
while True:
    soup = FuncCrawl.getSoupOfLink(site, 'utf-8', 'utf-8')
    # find interesting titles
    sourceName = '½»Í¨²¿'.decode('gbk')
    dictNewsSelected = {}
    #listTaga = soup.findAll('a', {'class':'titll_lk'})
    listTaga = soup.findAll('a', {'class':'titl_lk'})
    for taga in listTaga:
        textTime = taga.parent.parent.findAll('td')[2].findAll('li')[0].text
        matched = re.compile(r'(\d+)\D(\d+)\D(\d+)\D').match(textTime).groups()
        dtFromPage = datetime.datetime(
                int(matched[0]),
                int(matched[1]),
                int(matched[2])
                )
        FuncCrawl.fillDictNewsWithA(dictNewsSelected, taga, sourceName, dtFromPage)
    listDictOne = dictNewsSelected.values()
    print len(listDictOne)
    conn = FuncDB.connect(hostName, dbName, userName, password)
    FuncDB.insertWithListDictOne(conn, listDictOne, tbNameNews)
    conn.commit()
    conn.close()
    time.sleep(1)

    #site = url + '_' + str(n) + '.htm'
    site = url + str(n) + '&pubwebsite=zfxxgk&indexPa=1&schn=249&sinfo=249&surl=zfxxgk/249/list_4557_14.htm&curpos=%E6%9C%BA%E6%9E%84%E5%88%86%E7%B1%BB'
    n = n + 1
    print site

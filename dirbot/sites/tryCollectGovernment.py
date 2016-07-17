import FuncCrawl
import FuncDB
from dateutil.parser import parse
import time
import datetime
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

site = 'http://new.sousuo.gov.cn/list.htm?sort=pubtime&advance=true&t=paper&n=15'
while True:
    soup = FuncCrawl.getSoupOfLink(site, 'utf-8', 'utf-8')
    # find interesting titles
    sourceName = '¹úÎñÔº'.decode('gbk')
    dictNewsSelected = {}
    divSelected = soup.findAll('table', {'class':'dataList'})[0]
    for taga in divSelected.findAll('a'):
        pattern = re.compile(r'.*?/(\d+)-(\d+)/(\d+)/.*?')
        matched = pattern.match(taga.get('href')).groups()
        intYear = int(matched[0])
        intMonth = int(matched[1])
        intDay = int(matched[2])
        dtNow = datetime.datetime.now()
        dtFromPage = datetime.datetime(intYear, intMonth, intDay)
        FuncCrawl.fillDictNewsWithA(dictNewsSelected, taga, sourceName, dtFromPage)

    spanNextPage = soup.findAll('span', {'class':'wcm_pointer nav_go_next'})[0]
    tagaNextPage = spanNextPage.findAll('a')[0]
    site = tagaNextPage.attrs['href']
    print site

    listDictOne = dictNewsSelected.values()
    conn = FuncDB.connect(hostName, dbName, userName, password)
    FuncDB.insertWithListDictOne(conn, listDictOne, tbNameNews)
    conn.commit()
    conn.close()
    time.sleep(1)


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

listURL = []
url = 'http://www.miit.gov.cn/n11293472/n11293832/n11294072/n11302450/'
listURL.append(url)
url = 'http://www.miit.gov.cn/n11293472/n11293832/n13095885/'
listURL.append(url)
url = 'http://www.miit.gov.cn/n11293472/n11293832/n12843926/'
listURL.append(url)
url = 'http://www.miit.gov.cn/n11293472/n11293832/n12845605/n13916898/'
listURL.append(url)
url = 'http://www.miit.gov.cn/n11293472/n11293832/n12845605/n13916928/'
listURL.append(url)
url = 'http://www.miit.gov.cn/n11293472/n11293832/n12845605/n13916943/'
listURL.append(url)
url = 'http://www.miit.gov.cn/n11293472/n11293832/n12845605/n13916973/'
listURL.append(url)

'''
url = 'http://www.miit.gov.cn/n11293472/n11293832/n12845605/n13916913/'
listURL.append(url)
url = 'http://www.miit.gov.cn/n11293472/n11293832/n11293907/n11368223/'
listURL.append(url)
url = 'http://www.miit.gov.cn/n11293472/n11293832/n11293907/n12246780/'
listURL.append(url)
url = 'http://www.miit.gov.cn/n11293472/n11293832/n11293907/n11368277/'
listURL.append(url)
'''

for url in listURL:
    n = 1
    boolFirstPage = False
    year = None
    minMonth = 12
    boolSearchForDecember = True
    while True:
        if boolFirstPage is False:
            site = url + 'index_' + str(n) + '.html'
            n = n + 1
        else:
            site = url + 'index.html'
        print site
    
        soup = FuncCrawl.getSoupOfLink(site, 'utf-8', 'utf-8')
        # find interesting titles
        sourceName = '¹¤ÐÅ²¿'.decode('gbk')
        dictNewsSelected = {}
        divSelected = soup.findAll('table', {'class':'black14_24'})
        for tagtable in divSelected:
            # determine whether to retrieve year
            tagtds = tagtable.findAll('td')
            
            taga = tagtds[0].findAll('a')[0]
            linkAddress = taga.attrs['href']
            if linkAddress.find('miit.gov.cn') < 0:
                linkAddress = 'http://www.miit.gov.cn/' + linkAddress
                taga.attrs['href'] = linkAddress
            if year is None:
                
                dictOptions = {'link': linkAddress}
                year = FuncCrawl.parsePageGongxinbu(dictOptions)['datetime'].year

            textTime = tagtds[1].text
            patternMMDD = re.compile(r'^(\d+)-(\d+)$')
            matched = patternMMDD.match(textTime)

            if matched is None:
                dtFromPage = parse(tagtds[1].text)
            else:
                month = int(matched.groups()[0])
                day = int(matched.groups()[1])
                
                if month > minMonth and boolSearchForDecember:
                    minMonth = month
                    dictOptions = {'link': taga.attrs['href']}
                    try:
                        dictPage = FuncCrawl.parsePageGongxinbu(dictOptions)
                        year = dictPage['datetime'].year
                        boolSearchForDecember = False
                    except:
                        print 'Error\n\n\n\n'
                        continue

                if boolSearchForDecember == False and month <= minMonth:
                    boolSearchForDecember = True
                
                minMonth = min(minMonth, month)

                dtFromPage = datetime.datetime(
                        year,
                        month,
                        day
                        )
                
            print textTime, dtFromPage
            FuncCrawl.fillDictNewsWithA(dictNewsSelected, taga, sourceName, dtFromPage)
        listDictOne = dictNewsSelected.values()
        print len(listDictOne)
        
        if boolFirstPage is True:
            break
    
        conn = FuncDB.connect(hostName, dbName, userName, password)
        FuncDB.insertWithListDictOne(conn, listDictOne, tbNameNews)
        conn.commit()
        conn.close()
        time.sleep(1)
    
        if len(listDictOne) == 0:
            boolFirstPage = True
    

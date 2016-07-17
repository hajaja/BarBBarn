import FuncCrawl
import FuncDB
from dateutil.parser import parse
import time
import datetime
import re
import chardet
import pdb

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import selenium
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

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
tbNameNews = "tbBolaaikong"

browser = webdriver.Chrome()

datetimeStart = datetime.datetime(2016,1,1)
datetimeEnd = datetime.datetime(2016,1,10)
dtThis = datetimeStart
while dtThis <= datetimeEnd:
    yyyymm = dtThis.strftime('%Y%m')
    print yyyymm
    urlMonth = 'http://blog.sina.com.cn/s/article_archive_2042849783_' + yyyymm + '_1.html'
    import datetime
    dtThis = dtThis + datetime.timedelta(days=31)

    browser.get(urlMonth)
    time.sleep(10)
    listspan = browser.find_elements_by_css_selector('span.atc_title')
    
    listURL = []
    for span in listspan:
        url = span.find_element_by_tag_name('a').get_attribute('href')
        listURL.append(url)
   
    n = 0
    for url in listURL:
        time.sleep(10)
        n = n + 1
        if n > 3:
            #break
            pass
        
        # find interesting titles
        try:
            browser.get(url)
            title = browser.find_element_by_css_selector('h2.titName').text
        except:
            browser.get(url)
            try:
                title = browser.find_element_by_css_selector('h2.titName').text
            except:
                continue

        datetime = browser.find_element_by_css_selector('span.time').text
        datetime = datetime[1:-2]
        datetime = parse(datetime)
    
        divContent = browser.find_element_by_css_selector('div.articalContent')
        content = divContent.text
    
        sql='''
        INSERT INTO dbo.{3} VALUES(
        '{0}', 
        '{1}', 
        '{2}'
        )'''.format(
                title.encode('gbk', 'ignore'), 
                datetime.strftime('%Y-%m-%d %H:%M:%S'), 
                content.encode('gbk', 'ignore'),
                tbNameNews
                )
        
        conn = FuncDB.connect(hostName, dbName, userName, password)
        try:
            FuncDB.execute(conn, sql)
        except:
            pass
        conn.commit()
        conn.close()
    

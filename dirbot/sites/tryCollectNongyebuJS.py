import FuncCrawl
import FuncDB
from dateutil.parser import parse
import time
import datetime
import re

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
tbNameNews = "tbNewsHistory"
tbNameFulltext = "tbFulltextHistory"

#browser = webdriver.Firefox()
browser = webdriver.Chrome()

#url = 'http://www.moa.gov.cn/zwllm/tzgg/tz/index.htm'
url = 'http://www.moa.gov.cn/zwllm/tzgg/tfw/index_12.htm'
browser.get(url)
browser.implicitly_wait(30)

#listCheckbox = browser.find_elements_by_css_selector('dl.Mtable1.clearfix')[1].find_element_by_tag_name('dd').find_elements_by_tag_name('input')

dictNewsSelected = {}

while True:
    while True:
        try:
            divSelected = browser.find_element_by_css_selector('div.rlr')
            listLi = divSelected.find_elements_by_tag_name('li')
            break
        except:
            browser.refresh()
    for li in listLi:
        while True:
            try:
                taga = li.find_element_by_tag_name('a')
                span = li.find_elements_by_tag_name('span')[1]
                break
            except:
                time.sleep(10)
                pass
        
        textTime = re.compile('\((\d+\D\d+\D\d+)\)').match(span.text).groups()[0]
        dtFromPage = parse(textTime)
        title = taga.text
        linkAddress = taga.get_attribute('href')
        sourceName = 'Å©Òµ²¿'.decode('gbk')
        
        dictOne = {
                'title': title, 
                'datetime': dtFromPage, 
                'link': linkAddress,
                'source': sourceName,
                'keywords': []
                }
        print title.encode('gbk', 'ignore')
        dictNewsSelected[title] = dictOne
    
    listDictOne = dictNewsSelected.values()
    conn = FuncDB.connect(hostName, dbName, userName, password)
    FuncDB.insertWithListDictOne(conn, listDictOne, tbNameNews)
    conn.commit()
    conn.close()
    time.sleep(1)

    while True:
        try:
            listTaga = browser.find_element_by_css_selector('div#pageBar').find_elements_by_tag_name('a')
            break
        except:
            browser.refresh()
            print 'refreshed'
    taga = listTaga[-2]
    taga.click()
    browser.implicitly_wait(30)


import FuncCrawl
import FuncDB
from dateutil.parser import parse
import time
import datetime
import re
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
tbNameNews = "tbNewsHistory"
tbNameFulltext = "tbFulltextHistory"

#browser = webdriver.Firefox()
browser = webdriver.Chrome()
#url = 'http://www.zhb.gov.cn/zhxx/jrtt/index_13.htm'
#url = 'http://www.mep.gov.cn/zhxx/tz/index_16.htm'
url = 'http://www.mep.gov.cn/zwgk/hjgh/shierwu/index.htm'
browser.get(url)
browser.implicitly_wait(30)

#listCheckbox = browser.find_elements_by_css_selector('dl.Mtable1.clearfix')[1].find_element_by_tag_name('dd').find_elements_by_tag_name('input')

dictNewsSelected = {}

while True:
    while True:
        try:
            listTaga = browser.find_elements_by_css_selector('a.hh14')
            listTd = browser.find_elements_by_css_selector('td.data12')
            break
        except:
            pdb.set_trace()
            browser.refresh()
    for n in range(0, len(listTaga)):
        taga = listTaga[n]
        textTime = listTd[n].find_element_by_tag_name('span').text[1:-1]
        dtFromPage = parse(textTime)
        
        title = taga.text
        linkAddress = taga.get_attribute('href')
        sourceName = '»·±£²¿'.decode('gbk')
        
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
            listTaga = browser.find_elements_by_css_selector('a.zhlbjg12')
            break
        except:
            print 'refreshed'
            pdb.set_trace()
            browser.refresh()
    taga = listTaga[-2]
    taga.click()
    browser.implicitly_wait(30)


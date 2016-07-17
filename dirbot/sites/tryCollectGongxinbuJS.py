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
url = 'http://www.miit.gov.cn/n11293472/n11293832/n12843926/index.html'
browser.get(url)
browser.implicitly_wait(30)

#listCheckbox = browser.find_elements_by_css_selector('dl.Mtable1.clearfix')[1].find_element_by_tag_name('dd').find_elements_by_tag_name('input')

dictNewsSelected = {}

while True:
    while True:
        try:
            browser.switch_to_frame('searchList')
            listTable = browser.find_elements_by_css_selector('table.black14_24')
            break

        except:
            print 'to sleep'
            time.sleep(10)
    for n in range(0, len(listTable)):
        tr = listTable[n].find_element_by_tag_name('tbody').find_element_by_tag_name('tr')
        listTd = tr.find_elements_by_tag_name('td')
        taga = listTd[0].find_element_by_tag_name('a')
        textTime = listTd[1].text
        dtFromPage = parse(textTime)
        
        title = taga.text
        linkAddress = taga.get_attribute('href')
        sourceName = '¹¤ÐÅ²¿'.decode('gbk')
        
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
            listTaga = browser.find_element_by_css_selector('td.blue12_24').find_elements_by_tag_name('a')
            break
        except:
            print 'refreshed'
            pdb.set_trace()
            browser.refresh()
    taga = listTaga[-2]
    taga.click()
    browser.switch_to_default_content()
    browser.implicitly_wait(30)
    time.sleep(10)


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

#url = 'http://www.ndrc.gov.cn/jsWord/wjtype/201402/t20140220_588192.html'
#url = 'http://www.sdpc.gov.cn/jsWord/wjtype/201402/t20140220_588191.html'
#url = 'http://www.sdpc.gov.cn/jsWord/wjtype/201402/t20140220_588190.html'
#url = 'http://www.sdpc.gov.cn/jsWord/wjtype/201402/t20140220_588189.html'
url = 'http://www.sdpc.gov.cn/jsWord/wjtype/201402/t20140220_588188.html'
#url = 'http://www.sdpc.gov.cn/jsWord/wjtype/201402/t20140220_588187.html'
#url = 'http://www.sdpc.gov.cn/jsWord/wjtype/201402/t20140220_588186.html'
browser.get(url)
browser.implicitly_wait(30)

#listCheckbox = browser.find_elements_by_css_selector('dl.Mtable1.clearfix')[1].find_element_by_tag_name('dd').find_elements_by_tag_name('input')

dictNewsSelected = {}

while True:
    while True:
        try:
            listdl = browser.find_elements_by_css_selector('dl.list_04.clearfix')
            break
        except:
            browser.refresh()
    for dl in listdl:
        tagdd = dl.find_element_by_tag_name('dd')
        tagp = tagdd.find_elements_by_tag_name('p')[1]
        
        tagfont = tagp.find_element_by_tag_name('font')
        textTime = re.compile('\D*?(\d+\.\d+\.\d+)\D*?').match(tagfont.text).groups()[0]
        dtFromPage = parse(textTime)
        
        taga = tagp.find_element_by_tag_name('a')
        title = taga.get_attribute('title')
        linkAddress = taga.get_attribute('href')
        sourceName = '·¢¸ÄÎ¯'.decode('gbk')
        
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
            listTaga = browser.find_element_by_css_selector('li.L').find_elements_by_tag_name('a')
            break
        except:
            browser.refresh()
            print 'refreshed'
    taga = listTaga[-2]
    taga.click()
    browser.implicitly_wait(30)


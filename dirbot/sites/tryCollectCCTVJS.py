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
tbNameNews = "tbNewsHistory"
tbNameFulltext = "tbFulltextHistory"

#browser = webdriver.Firefox()
browser = webdriver.Chrome()

urlPrefix = 'http://cctv.cntv.cn/lm/xinwenlianbo/'
datetimeStart = datetime.datetime(2016, 1, 1)
datetimeEnd = datetime.datetime(2016, 1, 10)
datetimeThis = datetimeStart
dictNewsSelected = {}

boolSecondPage = False
while datetimeThis < datetimeEnd:
    print datetimeThis
    url = urlPrefix + datetimeThis.strftime('%Y%m%d') + '.shtml'
    if boolSecondPage == False:
        browser.get(url)

    listTaga = []
    while len(listTaga) == 0:
        while True:
            try:
                temp = browser.find_element_by_css_selector('div.title_list_box')
                break
            except:
                try:
                    temp = browser.find_element_by_css_selector('div.title_list_box_130503')
                    break
                except:
                    pass
            print 'to refresh'
            browser.refresh()
            time.sleep(5)

        listTaga = temp.find_elements_by_tag_name('a')
    
    for taga in listTaga:
        strToBeDeleted = '[��Ƶ]'.decode('gbk')
        title = taga.get_attribute('text')
        if chardet.detect(bytes(title))['encoding'].startswith('utf') is False:
            title = title.decode('gbk')
        title = title.replace(strToBeDeleted, '')

        linkAddress = taga.get_attribute('href')
        sourceName = '��������'.decode('gbk')
        dictOne = {
                'title': title, 
                'datetime': datetimeThis, 
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

    # second page
    try:
        divSelected = browser.find_element_by_css_selector('div.fy')
    except:
        divSelected = browser.find_element_by_css_selector('div.lvZ7967_ind14')

    listTaga = divSelected.find_elements_by_tag_name('a')

    if boolSecondPage is False and len(listTaga) > 5:
        listTaga[3].click()
        print 'second page clicked'
        boolSecondPage = True
    else:
        boolSecondPage = False
        datetimeThis = datetimeThis + datetime.timedelta(days=1)

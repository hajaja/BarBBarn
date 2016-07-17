# -*- coding: utf-8 -*-
import sys
import bs4,re
import datetime
import urllib2
import urllib
import requests
import requests.packages.chardet
import pdb
import threading
import time

from FuncParse import *
from dateutil.parser import parse

import httplib
import pytz

import selenium
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

#browserFagaiwei = webdriver.Firefox() # Get local session of firefox
#browserKejibu = webdriver.Firefox() # Get local session of firefox

def getSoupAndHeaders(linkAddress, encodingRequest, encodingSoup, proxy=None):
    toPrint = time.ctime() + ', start to get ' + linkAddress
    #print toPrint
    proxy = 'socks5://10.1.1.9:80'

    try: 
        numTimes = 0
        while numTimes < 3:
            try:
                if proxy is not None:
                    conn = httplib.HTTPConnection('10.1.1.9', 80)
                    conn.request('GET', linkAddress)
                    response = conn.getresponse()
                    html = response.read()
                    conn.close()
                else:
                    response = requests.get(linkAddress)
                    response.encoding = encodingRequest
                    html = response.text
                    response.close()
                break
            except:
                numTimes = numTimes + 1
                print 'to sleep'
                time.sleep(5)
    
        toPrint = time.ctime() + ', finish to get ' + linkAddress
        #print toPrint
        
        soup = bs4.BeautifulSoup(html, 'html.parser', from_encoding=encodingSoup)
        headers = response.getheaders()
        return [soup, headers]
    except: 
        print 'Error, in getSoupAndHeaders'
    
def getSoupOfLink(linkAddress, encodingRequest, encodingSoup, proxy=None):
    toPrint = time.ctime() + ', start to get ' + linkAddress
    #print toPrint
    proxy = 'socks5://10.1.1.9:80'

    try: 
        numTimes = 0
        while numTimes < 3:
            try:
                if proxy is not None:
                    conn = httplib.HTTPConnection('10.1.1.9', 80)
                    conn.request('GET', linkAddress)
                    response = conn.getresponse()
                    html = response.read()
                    conn.close()
                else:
                    response = requests.get(linkAddress)
                    response.encoding = encodingRequest
                    html = response.text
                    response.close()
                break
            except:
                numTimes = numTimes + 1
                time.sleep(5)
    
        toPrint = time.ctime() + ', finish to get ' + linkAddress
        #print toPrint
        
        soup = bs4.BeautifulSoup(html, 'html.parser', from_encoding=encodingSoup)
        return soup
    except: 
        print 'Error, in getSoupOfLink'
    
def getResponse(linkAddress, proxy=None):
    toPrint = time.ctime() + ', start to get ' + linkAddress
    #print toPrint
    proxy = 'socks5://10.1.1.9:80'

    try: 
        numTimes = 0
        while numTimes < 3:
            try:
                if proxy is not None:
                    conn = httplib.HTTPConnection('10.1.1.9', 80)
                    conn.request('GET', linkAddress)
                    response = conn.getresponse()
                    html = response.read()
                    conn.close()
                else:
                    response = requests.get(linkAddress)
                    response.encoding = encodingRequest
                    html = response.text
                    response.close()
                break
            except:
                numTimes = numTimes + 1
                time.sleep(5)
    
        return response
    except: 
        print 'Error, in getSoupOfLink'
    

def fillDictNewsWithA(dictNewsSelected, content, source, dt=None):
    if content.has_attr('href') == False:
        return
    if content.text == u'':
        return
    if len(content.text) <= 8:
        return
    if content.text[0] == content.text[1] and content.text[0] == content.text[2]:   # for CNStock
        return
    dictTemp = dict(content.attrs)
    strTitle = content.text
    strTitle.replace(u'\xa0', u' ')  #for CNStock
    strTitle = strTitle.replace('\n', '')  #for iFeng
    strTitle = strTitle.encode('gbk', 'ignore').decode('gbk')
    dictPieceContent = {}
    dictPieceContent['title'] = strTitle
    if source == '工信部'.decode('gbk'):
        dictPieceContent['link'] = 'http://www.miit.gov.cn' + dictTemp['href']
    else:
        dictPieceContent['link'] = dictTemp['href']

    if dt is None:
        dictPieceContent['datetime'] = datetime.datetime.now()
    else:
        dictPieceContent['datetime'] = dt

    dictPieceContent['source'] = source
    dictNewsSelected[strTitle] = dictPieceContent

class ClassThreadRetrieving(threading.Thread):
    def __init__(self, signal):
        threading.Thread.__init__(self)
        self.dictNews = {}
        self.dictThread = {}
        self.dictFunc = {
                'ifeng': retrieveNewsIfeng, 
                'sina': retrieveNewsSina,
                'cnstock': retrieveNewsCNStock,
                'people': retrieveNewsPeople,
                'cnstocklatest': retrieveNewsCNStockLatest,
                'government': retrieveNewsGovernment,
                'stcn': retrieveNewsStcn,
                'gongxinbu': retrieveNewsGongxinbu,
                'caizhengbu': retrieveNewsCaizhengbu,
                'fagaiwei': retrieveNewsFagaiwei2,
                
                'shengyishe': retrieveNewsShengyishe
                }
        self.signal = signal
        for threadName in self.dictFunc:
            self.dictThread[threadName] = ClassThreadRetrieveNews(threadName, self.dictFunc[threadName])
            self.dictThread[threadName].setDaemon(True)
            self.dictThread[threadName].start()

    def setParameters(self):
        pass

    def run(self):
        while True:
            #print 'start retrievNews ', time.ctime()
            self.signal.wait()
            self.signal.clear()
            self.retrieveNews()
            self.signal.set()
            #time.sleep(30)

    def retrieveNews(self):
        listActiveThreadName = []
        for thread in threading.enumerate():
            listActiveThreadName.append(thread.getName())
        for threadName in self.dictThread:
            if threadName not in listActiveThreadName:
                self.dictNews.update(self.dictThread[threadName].dictNews)
                self.dictThread[threadName] = ClassThreadRetrieveNews(threadName, self.dictFunc[threadName])
                self.dictThread[threadName].setDaemon(True)
                self.dictThread[threadName].start()


class ClassThreadRetrieveNews(threading.Thread):
    def __init__(self, name, func):
        threading.Thread.__init__(self, name=name)
        self.dictNews = {}
        self.func = func
    def run(self):
        self.dictNews.update(self.func())

def retrieveNewsCNStock():
    site = 'http://www.cnstock.com/'
    soup = getSoupOfLink(site, 'utf-8', 'utf-8')
    sourceName = '中证网'.decode('gbk')
    #site = 'file:./cnstock.html'    
    # find interesting titles
    # top-area
    divSelected = soup.findAll('div', {'class':'top-area'})[0] 
    dictNewsSelected = {}
    list = [];
    for tag in divSelected.findAll('h1'):
        for taga in tag.findAll('a'):
            fillDictNewsWithA(dictNewsSelected, taga, sourceName)
    for tag in divSelected.findAll('h4'):
        for taga in tag.findAll('a'):
            fillDictNewsWithA(dictNewsSelected, taga, sourceName)
    # top-list
    divSelected = soup.findAll('div', {'class':'top-list'}) 
    for tagdiv in divSelected:
        for taga in tagdiv.findAll('a'):
            fillDictNewsWithA(dictNewsSelected, taga, sourceName)
    
    # find the latest news
    return dictNewsSelected

def retrieveNewsSina():
    site = 'http://finance.sina.com.cn/'
    soup = getSoupOfLink(site, 'utf-8', 'utf-8')
    sourceName = '新浪'.decode('gbk')

    # find interesting titles
    # 'data-client':'scroll important'
    dictNewsSelected = {}
    divSelected = soup.findAll('div', {'id':'blk_hdline_01'})
    for taga in divSelected[0].findAll('a'):
        fillDictNewsWithA(dictNewsSelected, taga, sourceName)
    
    divSelected = soup.findAll('div', {'data-client':'scroll important'})
    for taga in divSelected[0].findAll('a'):
        fillDictNewsWithA(dictNewsSelected, taga, sourceName)
    
    divSelected = soup.findAll('div', {'data-sudaclick':'blk_yw_zq_01_1'})
    for taga in divSelected[0].findAll('a'):
        fillDictNewsWithA(dictNewsSelected, taga, sourceName)

    divSelected = soup.findAll('div', {'data-sudaclick':'blk_yw_zq_01_2'})
    for taga in divSelected[0].findAll('a'):
        fillDictNewsWithA(dictNewsSelected, taga, sourceName)

    divSelected = soup.findAll('div', {'data-sudaclick':'blk_yw_zq_01_3'})
    for taga in divSelected[0].findAll('a'):
        fillDictNewsWithA(dictNewsSelected, taga, sourceName)

    divSelected = soup.findAll('ul', {'data-sudaclick':'blk_yw_zq_01_4'})
    for taga in divSelected[0].findAll('a'):
        fillDictNewsWithA(dictNewsSelected, taga, sourceName)

    # find the latest news
    return dictNewsSelected

def retrieveNewsIfeng():
    sourceName = '凤凰'.decode('gbk')
    dictNewsSelected = {}

    # headline
    site = 'http://finance.ifeng.com/'
    soup = getSoupOfLink(site, 'utf-8', 'utf-8')
    divSelected = soup.findAll('div', {'class':'box_01'})
    for n in range(0, len(divSelected)):
        for taga in divSelected[n].findAll('a'):
            fillDictNewsWithA(dictNewsSelected, taga, sourceName)
    
    # policy
    site = 'http://finance.ifeng.com/macro/policy/'
    soup = getSoupOfLink(site, 'utf-8', 'utf-8')
    divSelected = soup.findAll('div', {'class':'box_list'})
    listli = divSelected[0].findAll('li')
    for li in listli:
        divDate = li.findAll('div', {'class':'date'})[0]
        dtFromPage = parse(divDate.text)
        taga = li.findAll('h3')[0].findAll('a')[0]
        fillDictNewsWithA(dictNewsSelected, taga, sourceName, dtFromPage)

    # fhbp 
    site = 'http://finance.ifeng.com/stock/fhbp/'
    soup = getSoupOfLink(site, 'utf-8', 'utf-8')
    divSelected = soup.findAll('div', {'class':'box_list'})
    listli = divSelected[0].findAll('li')
    for li in listli:
        divDate = li.findAll('div', {'class':'date'})[0]
        dtFromPage = parse(divDate.text)
        taga = li.findAll('h3')[0].findAll('a')[0]
        fillDictNewsWithA(dictNewsSelected, taga, sourceName, dtFromPage)

    # ssgs
    site = 'http://finance.ifeng.com/stock/ssgs/'
    soup = getSoupOfLink(site, 'utf-8', 'utf-8')
    divSelected = soup.findAll('div', {'class':'box_list'})
    listli = divSelected[0].findAll('li')
    for li in listli:
        divDate = li.findAll('div', {'class':'date'})[0]
        dtFromPage = parse(divDate.text)
        taga = li.findAll('h3')[0].findAll('a')[0]
        fillDictNewsWithA(dictNewsSelected, taga, sourceName, dtFromPage)
    
    return dictNewsSelected

def retrieveNewsPeople():
    site = 'http://www.people.com.cn/'
    soup = getSoupOfLink(site, 'gbk', 'gbk')
    sourceName = '人民网'.decode('gbk')
    # find interesting titles
    # 'data-client':'scroll important'
    dictNewsSelected = {}

    divSelected = soup.findAll('div', {'class':'main_h'})
    for taga in divSelected[0].findAll('a'):
        fillDictNewsWithA(dictNewsSelected, taga, sourceName)

    divSelected = soup.findAll('div', {'class':'focus'})
    for taga in divSelected[0].findAll('a'):
        fillDictNewsWithA(dictNewsSelected, taga, sourceName)

    divSelected = soup.findAll('div', {'id':'list_new_c_1'})
    for taga in divSelected[0].findAll('a'):
        fillDictNewsWithA(dictNewsSelected, taga, sourceName)
        
    # find the latest news
    return dictNewsSelected

def retrieveNewsCNStockLatest():
    toPrint = 'start to retrieve CNStockLatest' + time.ctime()
    #print toPrint
    site = 'http://news.cnstock.com/gdxw/v_industry/sid_cyzh/201306/null'
    soup = getSoupOfLink(site, 'utf-8', 'utf-8')
        # find interesting titles
    sourceName = '上证快讯'.decode('gbk')
    dictNewsSelected = {}
    divSelected = soup.findAll('ul', {'id':'bw-list'})
    for divTitle in divSelected[0].findAll('div', {'class':'title'}):
        textTime = divTitle.findAll('span')[0].text
        pattern = re.compile(r'(\d\d)\:(\d\d)')
        matched = pattern.match(textTime).groups()
        intHour = int(matched[0])
        intMinute = int(matched[1])
        dtNow = datetime.datetime.now()
        if datetime.time(intHour, intMinute) > dtNow.time():
            # news of yesterday
            dtYesterday = dtNow - datetime.timedelta(1)
            dtFromPage = datetime.datetime(dtYesterday.year, dtYesterday.month, dtYesterday.day, intHour, intMinute)
        else:
            dtFromPage = datetime.datetime(dtNow.year, dtNow.month, dtNow.day, intHour, intMinute)
        taga = divTitle.findAll('a')[0]
        if type(taga.contents[0]) is not bs4.element.Tag:
            fillDictNewsWithA(dictNewsSelected, taga, sourceName, dtFromPage)
        else:
            if taga.contents[0].name == 'font':
                fillDictNewsWithA(dictNewsSelected, taga, sourceName, dtFromPage)
    toPrint = 'finish to retrieve CNStockLatest' + time.ctime()
    #print toPrint
    return dictNewsSelected

def retrieveNewsGovernment():
    site = 'http://new.sousuo.gov.cn/list.htm?sort=pubtime&advance=true&t=paper&n=15'
    soup = getSoupOfLink(site, 'utf-8', 'utf-8')
    # find interesting titles
    sourceName = '国务院'.decode('gbk')
    dictNewsSelected = {}
    divSelected = soup.findAll('table', {'class':'dataList'})[0]
    for taga in divSelected.findAll('a'):
        pattern = re.compile(r'.*?/(\d+)-(\d+)/(\d+)/.*?')
        matched = pattern.match(taga.get('href')).groups()
        intYear = int(matched[0])
        intMonth = int(matched[1])
        intDay = int(matched[2])
        dtNow = datetime.datetime.now()
        dtFromPage = datetime.datetime(intYear, intMonth, intDay, dtNow.hour, dtNow.minute)
        fillDictNewsWithA(dictNewsSelected, taga, sourceName, dtFromPage)
    return dictNewsSelected

def retrieveNewsStcn():
    site = 'http://kuaixun.stcn.com/index_1.shtml'
    soup = getSoupOfLink(site, 'utf-8', 'utf-8')
    # find interesting titles
    sourceName = '证券时报'.decode('gbk')
    dictNewsSelected = {}
    divSelected = soup.findAll('div', {'id':'mainlist'})[0]
    for tagp in divSelected.findAll('p', {'class':'tit'}):
        taga = tagp.findAll('a')[1]
        tagspan = tagp.findAll('span')[0]
        dtFromPage = parse(tagspan.text[1:-1])
        fillDictNewsWithA(dictNewsSelected, taga, sourceName, dtFromPage)
    return dictNewsSelected

def retrieveNewsGongxinbu():
    site = 'http://www.miit.gov.cn/n11293472/n11293832/n13095885/index.html'
    soup = getSoupOfLink(site, 'utf-8', 'utf-8')
    # find interesting titles
    sourceName = '工信部'.decode('gbk')
    dictNewsSelected = {}
    divSelected = soup.findAll('table', {'class':'black14_24'})
    for tagtable in divSelected:
        tagtds = tagtable.findAll('td')
        taga = tagtds[0].findAll('a')[0]
        dtFromPage = parse(tagtds[1].text)
        dtFromPage = datetime.datetime.now()
        fillDictNewsWithA(dictNewsSelected, taga, sourceName, dtFromPage)
    return dictNewsSelected

def retrieveNewsCaizhengbu():
    site = 'http://www.mof.gov.cn/zhengwuxinxi/caizhengxinwen/'
    soup = getSoupOfLink(site, 'gbk', 'gbk')
    # find interesting titles
    sourceName = '财政部'.decode('gbk')
    dictNewsSelected = {}
    divSelected = soup.findAll('table', {'class':'ZIT'})[0].findAll('td', {'class':'ZITI'})
    for tagtd in divSelected:
        taga = tagtd.findAll('a')[0]
        pattern = re.compile(r'.*?(\d+-\d+-\d+).*?', re.S)
        matched = pattern.match(tagtd.text)
        textTime = datetime.datetime.now().strftime('%H%M%S')
        dtFromPage = parse(matched.groups()[0] + ' ' + textTime)
        taga.attrs['href'] = site + taga.attrs['href']
        fillDictNewsWithA(dictNewsSelected, taga, sourceName, dtFromPage)
    return dictNewsSelected

def retrieveNewsFagaiwei():
    url = 'http://www.sdpc.gov.cn/govszyw/'
    dictNewsSelected = {}
    browser = browserFagaiwei
    browser.get(url) # Load page
    print 'wait to finish loading'
    browser.implicitly_wait(30)
    #time.sleep(5) # Let the page load

    listLi = browserFagaiwei.find_elements_by_class_name('govpushinfo150203')[0].find_elements_by_tag_name('li')
    for li in listLi:
        taga = li.find_element_by_tag_name('a')
        title = taga.text
        linkAddress = taga.get_attribute('href')
        source = '发改委'.decode('gbk')
        textTime = li.find_element_by_tag_name('span').text
        dtFromPage = datetime.datetime.now()
        dictOne = {
                'title': title, 
                'datetime': dtFromPage, 
                'link': linkAddress,
                'source': source,
                'keywords': []
                }
        dictNewsSelected[title] = dictOne
    
    return dictNewsSelected

def retrieveNewsFagaiwei2():
    site = 'http://www.sdpc.gov.cn/gzdt/'
    soup = getSoupOfLink(site, 'utf-8', 'utf-8')
    # find interesting titles
    sourceName = '发改委'.decode('gbk')
    dictNewsSelected = {}
    divSelected = soup.findAll('li', {'class':'li'})
    for tagli in divSelected:
        tagfont = tagli.findAll('font')[0]
        #dtFromPage = parse(tagfont.text)
        dtFromPage = datetime.datetime.now()
        taga = tagli.findAll('a')[0]
        taga.attrs['href'] = site + taga.attrs['href']
        fillDictNewsWithA(dictNewsSelected, taga, sourceName, dtFromPage)

    site = 'http://ghs.ndrc.gov.cn/zttp/135ghbzgz/'
    soup = getSoupOfLink(site, 'utf-8', 'utf-8')
    sourceName = '发改委'.decode('gbk')
    divSelected = soup.findAll('li', {'class':'li'})
    for tagli in divSelected:
        tagfont = tagli.findAll('font')[0]
        #dtFromPage = parse(tagfont.text)
        dtFromPage = datetime.datetime.now()
        taga = tagli.findAll('a')[0]
        taga.attrs['href'] = site + taga.attrs['href']
        fillDictNewsWithA(dictNewsSelected, taga, sourceName, dtFromPage)

    site = 'http://www.sdpc.gov.cn/zcfb/zcfbl/'
    soup = getSoupOfLink(site, 'utf-8', 'utf-8')
    sourceName = '发改委'.decode('gbk')
    divSelected = soup.findAll('li', {'class':'li'})
    for tagli in divSelected:
        tagfont = tagli.findAll('font')[0]
        #dtFromPage = parse(tagfont.text)
        dtFromPage = datetime.datetime.now()
        taga = tagli.findAll('a')[0]
        taga.attrs['href'] = site + taga.attrs['href']
        fillDictNewsWithA(dictNewsSelected, taga, sourceName, dtFromPage)

    site = 'http://www.sdpc.gov.cn/zcfb/zcfbgg/'
    soup = getSoupOfLink(site, 'utf-8', 'utf-8')
    sourceName = '发改委'.decode('gbk')
    divSelected = soup.findAll('li', {'class':'li'})
    for tagli in divSelected:
        tagfont = tagli.findAll('font')[0]
        #dtFromPage = parse(tagfont.text)
        dtFromPage = datetime.datetime.now()
        taga = tagli.findAll('a')[0]
        taga.attrs['href'] = site + taga.attrs['href']
        fillDictNewsWithA(dictNewsSelected, taga, sourceName, dtFromPage)

    site = 'http://www.sdpc.gov.cn/zcfb/zcfbghwb/'
    soup = getSoupOfLink(site, 'utf-8', 'utf-8')
    sourceName = '发改委'.decode('gbk')
    divSelected = soup.findAll('li', {'class':'li'})
    for tagli in divSelected:
        tagfont = tagli.findAll('font')[0]
        #dtFromPage = parse(tagfont.text)
        dtFromPage = datetime.datetime.now()
        taga = tagli.findAll('a')[0]
        taga.attrs['href'] = site + taga.attrs['href']
        fillDictNewsWithA(dictNewsSelected, taga, sourceName, dtFromPage)

    site = 'http://www.sdpc.gov.cn/zcfb/zcfbtz/'
    soup = getSoupOfLink(site, 'utf-8', 'utf-8')
    sourceName = '发改委'.decode('gbk')
    divSelected = soup.findAll('li', {'class':'li'})
    for tagli in divSelected:
        tagfont = tagli.findAll('font')[0]
        #dtFromPage = parse(tagfont.text)
        dtFromPage = datetime.datetime.now()
        taga = tagli.findAll('a')[0]
        taga.attrs['href'] = site + taga.attrs['href']
        fillDictNewsWithA(dictNewsSelected, taga, sourceName, dtFromPage)
    
    site = 'http://www.sdpc.gov.cn/zcfb/jd/'
    soup = getSoupOfLink(site, 'utf-8', 'utf-8')
    sourceName = '发改委'.decode('gbk')
    divSelected = soup.findAll('li', {'class':'li'})
    for tagli in divSelected:
        tagfont = tagli.findAll('font')[0]
        #dtFromPage = parse(tagfont.text)
        dtFromPage = datetime.datetime.now()
        taga = tagli.findAll('a')[0]
        taga.attrs['href'] = site + taga.attrs['href']
        fillDictNewsWithA(dictNewsSelected, taga, sourceName, dtFromPage)
    
    site = 'http://www.sdpc.gov.cn/zcfb/zcfbqt/'
    soup = getSoupOfLink(site, 'utf-8', 'utf-8')
    sourceName = '发改委'.decode('gbk')
    divSelected = soup.findAll('li', {'class':'li'})
    for tagli in divSelected:
        tagfont = tagli.findAll('font')[0]
        #dtFromPage = parse(tagfont.text)
        dtFromPage = datetime.datetime.now()
        taga = tagli.findAll('a')[0]
        taga.attrs['href'] = site + taga.attrs['href']
        fillDictNewsWithA(dictNewsSelected, taga, sourceName, dtFromPage)
    
    return dictNewsSelected

def retrieveNewsKejibu():
    url = 'http://www.most.gov.cn//mostinfo/xinxifenlei/zjgx/index.htm'
    dictNewsSelected = {}
    browser = browserKejibu
    browser.get(url) # Load page
    print 'wait to finish loading'
    browser.implicitly_wait(30)
    listTaga = browser.find_elements_by_css_selector('a.STYLE30')

    for taga in listTaga:
        title = taga.text
        linkAddress = taga.get_attribute('href')
        source = '科技部'.decode('gbk')
        print linkAddress
        response = getResponse(linkAddress)
        dictHeader = dict(response.getheaders())
        dtFromPage = parse(dictHeader['last-modified'])
        dtFromPage = dtFromPage.astimezone(pytz.timezone('Asia/Shanghai'))
        dictOne = {
                'title': title, 
                'datetime': dtFromPage, 
                'link': linkAddress,
                'source': source,
                'keywords': []
                }
        dictNewsSelected[title] = dictOne
    
    return dictNewsSelected

def retrieveNewsShengyishe():
    site = 'http://chem.100ppi.com/news/list---1.html'
    soup = getSoupOfLink(site, 'utf-8', 'utf-8')
    # find interesting titles
    sourceName = '生意社'.decode('gbk')
    dictNewsSelected = {}
    divSelected = soup.findAll('div', {'class':'list-c'})[0]
    for tagli in divSelected.findAll('li'):
        taga = tagli.findAll('a')[1]
        tagspan = tagli.findAll('span')[0]
        dtFromPage = parse(tagspan.text)
        fillDictNewsWithA(dictNewsSelected, taga, sourceName, dtFromPage)
    return dictNewsSelected

class ClassThreadParsePage(threading.Thread):
    def __init__(self, name, func, dictOptions):
        threading.Thread.__init__(self, name=name)
        self.dictRet = {}
        self.func = func
        self.dictOptions = dictOptions
    def run(self):
        self.dictRet.update(self.func(self.dictOptions))

def parsePageStockLatest(dictOptions):
    toPrint = 'start to parse' + dictOptions['link'] + time.ctime()
    print toPrint
    linkAddress = dictOptions['link']
    listKeyWordsPositive = dictOptions['listKeyWordsPositive']
    soup = getSoupOfLink(linkAddress, 'gbk', 'gbk')
    pSelected = soup.findAll('div', {'id':'qmt_content_div'})[0]
    text = ''
    for p in pSelected:
        try:
            pText = p.text
        except:
            pText = ''
        text = text + pText
    listKeyWordsCollected = filterByKeyWords(text, listKeyWordsPositive)
    spanSelected = soup.findAll('span', {'class': 'timer'})
    if len(spanSelected) != 0:
        spanTimeSelected = spanSelected[0]
    else:
        spanTimeSelected = soup.findAll('span', {'class': 'time'})[0]

    datetimeParsed = parse(spanTimeSelected.text)
    dictRet = {
            'listKeyWordsCollected': listKeyWordsCollected,
            'datetime': datetimeParsed,
            'fulltext': text
            }
    toPrint = 'finish to parse' + dictOptions['link'] + time.ctime()
    print toPrint
    return dictRet

def retrieveNewsCNStockLatestHistory(site):
    soup = getSoupOfLink(site, 'utf-8', 'utf-8')
        # find interesting titles
    sourceName = '上证快讯'.decode('gbk')
    dictNewsSelected = {}
    divSelected = soup.findAll('ul', {'id':'bw-list'})
    if len(divSelected) == 0:
        return None

    for divTitle in divSelected[0].findAll('div', {'class':'title'}):
        taga = divTitle.findAll('a')[0]
        if type(taga.contents[0]) is not bs4.element.Tag:
            fillDictNewsWithA(dictNewsSelected, taga, sourceName)
        else:
            if taga.contents[0].name == 'font':
                fillDictNewsWithA(dictNewsSelected, taga, sourceName)
    return dictNewsSelected

def parsePageSina(dictOptions):
    linkAddress = dictOptions['link']
    listKeyWordsPositive = dictOptions['listKeyWordsPositive']
    soup = getSoupOfLink(linkAddress, 'gbk', 'gbk')
    divSelected = soup.findAll('div', {'id':'artibody'})[0]
    pSelected = divSelected.findAll('p')
    text = ''
    for p in pSelected:
        try:
            pText = p.text
        except:
            pText = ''
        text = text + pText
    listKeyWordsCollected = filterByKeyWords(text, listKeyWordsPositive)
    spanSelected = soup.findAll('span', {'id': 'pub_date'})
    if len(spanSelected) != 0:
        spanTimeSelected = spanSelected[0]
    else:
        spanTimeSelected = soup.findAll('span', {'class': 'time'})[0]

    textDateTime = spanTimeSelected.text
    pattern = re.compile(r'(\d+)\D*?(\d+)\D*?(\d+)\D*?(\d+):(\d+)')
    matched = pattern.match(textDateTime)
    #print matched.groups()
    listMatched = matched.groups()
    datetimeParsed = datetime.datetime(
            int(listMatched[0]), 
            int(listMatched[1]), 
            int(listMatched[2]), 
            int(listMatched[3]), 
            int(listMatched[4])
            )

    dictRet = {
            'listKeyWordsCollected': listKeyWordsCollected,
            'datetime': datetimeParsed,
            'fulltext': text
            }
    return dictRet

def parsePageGongxinbu(dictOptions):
    toPrint = 'start to parse' + dictOptions['link'] + time.ctime()
    print toPrint
    linkAddress = dictOptions['link']
    listLink = getSoupAndHeaders(linkAddress, 'utf-8', 'utf-8')
    soup = listLink[0]
    dictHeaders = dict(listLink[1])
    datetimeLastModified = parse(dictHeaders['last-modified'])
    datetimeLastModified = datetimeLastModified.astimezone(pytz.timezone('Asia/Shanghai'))
    
    td = soup.findAll('td', {'id':'Zoom2'})[0]
    text = td.text
    
    textTime = soup.findAll('td', {'class':'main-lm2'})[0].text
    matched = re.compile(r'.*?(\d+)\D(\d+)\D(\d+)\D.*?').match(textTime)
    listMatched = matched.groups()
    datetimeParsed = datetime.datetime(
            int(listMatched[0]),
            int(listMatched[1]),
            int(listMatched[2])
            )
    if (datetimeLastModified.date() - datetimeParsed.date()).days == 0:
        datetimeParsed = datetime.datetime(
                datetimeParsed.year,
                datetimeParsed.month,
                datetimeParsed.day,
                datetimeLastModified.hour,
                datetimeLastModified.minute,
                datetimeLastModified.second
                )
    dictRet = {
            'datetime': datetimeParsed,
            'fulltext': text
            }
    toPrint = 'finish to parse' + dictOptions['link'] + time.ctime()
    print toPrint
    return dictRet

#aa = retrieveNewsKejibu()
#aa = retrieveNewsFagaiwei2()

#dictOptions = {'link': 'http://www.miit.gov.cn/n11293472/n11293832/n11293907/n11368223/12962211.html'}
#aa = parsePageGongxinbu(dictOptions)

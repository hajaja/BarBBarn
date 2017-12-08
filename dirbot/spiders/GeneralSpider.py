import scrapy
from dirbot.items import Website, News
import dirbot.settings
import datetime
import logging
import dateutil.parser
import traceback
import re
import time

import Utils
reload(Utils)

class GeneralSpider(scrapy.Spider):
    name = 'GeneralSpider'
    start_urls = [
            'http://finance.sina.com.cn/',
            'http://finance.ifeng.com/',
            'http://finance.qq.com/',
            #'http://business.sohu.com/',
            #'http://www.cnstock.com/',
            'http://www.caijing.com.cn/',
            'http://www.jrj.com.cn/',
            'http://www.yicai.com/',
            'http://www.10jqka.com.cn/',
            'http://www.eastmoney.com/',
            ]
    def parse(self, response):
        self.download_delay = 0.5
        self.random_download_delay = False
        # find all <a>
        listTaga = []
        try:
            listTagaTemp = response.css('a')
            for taga in listTagaTemp:
                text = taga.css('::text').extract_first()
                if text is not None and len(text) > 6:
                    listTaga.append(taga)
        except:
            logging.log(logging.ERROR, 'Home page parse error')
            logging.exception(self.source)
            return

        print 'TOTAL A: %d'%(len(listTaga))
        
        # crawl taga
        for taga in listTaga:
            full_url = taga.css('::attr(href)').extract_first().strip()
            if full_url.startswith('//'):
                full_url = 'http:' + full_url
                logging.log(logging.ERROR, 'double slash: %s'%full_url)
            title = taga.css('::text').extract_first()
            try:
                yield scrapy.Request(full_url, callback=self.parse_page, meta={'title': title})
            except:
                logging.log(logging.ERROR, 'full_url error: %s'%full_url)
        
        '''
        # next page
        if dirbot.settings.DICT_SWITCH['SZKX']['HISTORY'] is True:
            strNextPage = u'\u4e0b\u4e00\u9875'
            urlNextPage = response.xpath(u'//a[text()="%s"]/@href'%strNextPage).extract_first()
            if urlNextPage is not None:
                yield scrapy.Request(urlNextPage, callback=self.parse)
        '''

    def parse_page(self, response):
        if response is None:
            logging.log(logging.ERROR, 'null response')
            return
        
        title = response.meta['title']
        dtCreated = None
        source = self.parseSource(response)
        
        try:
            if source is 'Sina':
                dtCreated = response.css('span[class="time-source"]::text').extract_first()
                if dtCreated is None:
                    # http://finance.sina.com.cn/zl/stock/20160616/082024822271.shtml
                    dtCreated = response.css('span[class="pub_date"]::text').extract_first()
                if dtCreated is None:
                    # http://finance.sina.com.cn/zl/china/2017-12-08/zl-ifyppemf5823126.shtml
                    dtCreated = response.css('span[id="pub_date"]::text').extract_first()
                if dtCreated is None:
                    # http://finance.sina.com.cn/zl/stock/20160616/082024822271.shtml
                    dtCreated = response.css('span[class="time"]::text').extract_first()
                if dtCreated is None:
                    # http://collection.sina.com.cn/cqyw/2017-12-05/doc-ifyphxwa7893955.shtml
                    dtCreated = response.css('span[class="titer"]::text').extract_first()
                if dtCreated is None:
                    # http://blog.sina.com.cn/u/1197890497
                    dtCreated = response.css('span[class="time SG_txtc"]::text').extract_first()[1:-1]
                dtCreated = Utils.parseDT(dtCreated)
                text = response.css('div[id="artibody"]').css('::text').extract()
                text = ' '.join(text)
                text = re.sub('[\s\t\n][\s\t\n]+', '', text)
            elif source is 'Ifeng':
                dtCreated = response.css('span[class="ss01"]::text').extract_first()
                dtCreated = Utils.parseDT(dtCreated)
                text = response.css('div[id="main_content"]').css('::text').extract()
                text = ' '.join(text)
                text = re.sub('[\s\t\n][\s\t\n]+', '', text)
            elif source is 'QQ':
                dtCreated = response.css('span[class="a_time"]::text').extract_first()
                dtCreated = Utils.parseDT(dtCreated)
                text = response.css('div[id="Cnt-Main-Article-QQ"]').css('::text').extract()
                text = ' '.join(text)
                text = re.sub('[\s\t\n][\s\t\n]+', '', text)
            elif source is 'Sohu':
                dtCreated = response.css('div[class="time"]::text').extract_first()
                dtCreated = Utils.parseDT(dtCreated)
                text = response.css('div[itemprop="article"]').css('::text').extract()
                text = ' '.join(text)
                text = re.sub('[\s\t\n][\s\t\n]+', '', text)
            elif source is 'CNStock':
                if title is None:
                    title = response.css('h1::text').extract_first()
                dtCreated = response.css('span[class="timer"]::text').extract_first()
                if dtCreated is None:
                    dtCreated = response.css('span[class="time"]').extract_first()
                if dtCreated is None:
                    dtCreated = response.css('div[class="ll-time"]').extract_first()
                if dtCreated is None:
                    dtCreated = response.css('p[class="time"]').extract_first()
                if dtCreated is None:
                    logging.log(logging.DEBUG, response)
                dtCreated = Utils.parseDT(dtCreated)
                text = response.css('div[id="qmt_content_div"]').css('p::text').extract()
                text = ' '.join(text)
            elif source is 'Caijing':
                dtCreated = response.css('span[id="pubtime_baidu"]::text').extract_first()
                dtCreated = Utils.parseDT(dtCreated)
                text = response.css('div[id="the_content"]').css('::text').extract()
                text = ' '.join(text)
                pass
            elif source is 'JRJ':
                dtCreated = response.css('p[class="inftop"]>span')[0].css('::text').extract_first()
                dtCreated = Utils.parseDT(dtCreated)
                text = response.css('div[class="texttit_m1"]').css('::text').extract()
                text = ' '.join(text)
                pass
            elif source is 'Caijing':
                dtCreated = response.css('span[id="pubtime_baidu"]::text').extract_first()
                if dtCreated is None:
                    dtCreated = response.css('span[class="news_time"]::text').extract_first()
                dtCreated = Utils.parseDT(dtCreated)
                text = response.css('div[id="the_content"]').css('::text').extract()
                text = ' '.join(text)
                pass
            elif source is 'JRJ':
                dtCreated = response.css('p[class="inftop"]>span')[0].css('::text').extract_first()
                dtCreated = Utils.parseDT(dtCreated)
                text = response.css('div[class="texttit_m1"]').css('::text').extract()
                text = ' '.join(text)
                pass
            elif source is 'CBN':
                dtCreated = response.css('h2>span')[1].css('::text').extract_first()
                if dtCreated is None:
                    dtCreated = response.css('h3[class="f-fs24 f-tac"]>span')[1].css('::text').extract_first()
                dtCreated = Utils.parseDT(dtCreated)
                text = response.css('div[class="m-text"]').css('::text').extract()
                text = ' '.join(text)
            elif source is 'THS':
                dtCreated = response.css('span[id="pubtime_baidu"]::text').extract_first()
                dtCreated = Utils.parseDT(dtCreated)
                text = response.css('div[class="atc_content"]').css('::text').extract()
                text = ' '.join(text)
                pass
            elif source is 'EastMoney':
                dtCreated = response.css('div[class="time"]>span')[0].css('::text').extract_first()
                dtCreated = Utils.parseDT(dtCreated)
                text = response.css('div[class="ContentBody"]').css('::text').extract()
                text = ' '.join(text)
                pass
            else:
                logging.log(logging.INFO, response.url)
                raise Exception('Unknown Source')

        except Exception:
            logging.exception('Exception: %s'%response.url)
            title = response.meta['title']
            dtCreated = 'NULL'
            text = response.css('p::text').extract()
            text = ' '.join(text)

        item = News()
        item['title'] = title
        item['dtCreated'] = dtCreated 
        item['text'] = text
        item['url'] = response.url
        item['source'] = source
        item['dtCrawled'] = datetime.datetime.now()
        yield item
	    
    def parseSource(self, response):
        url = response.url
        if 'sina.com' in url:
            source = 'Sina'
        elif 'ifeng.com' in url:
            source = 'Ifeng'
        elif 'qq.com' in url:
            source = 'QQ'
        elif 'sohu.com' in url:
            source = 'Sohu'
        elif 'cnstock.com' in url:
            source = 'CNStock'
        elif 'caijing.com' in url:
            source = 'Caijing'
        elif 'jrj.com' in url:
            source = 'JRJ'
        elif 'yicai.com' in url:
            source = 'CBN'
        elif '10jqka.com' in url:
            source = 'THS'
        elif 'eastmoney.com' in url:
            source = 'EastMoney'
        else:
            source = url
        return source


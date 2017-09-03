import scrapy
from dirbot.items import Website, News
import dirbot.settings
import datetime
import logging
import dateutil.parser
import traceback
import re

def buildItem(taga, source, dictSettings={}):
    item = News()
    item['title'] = taga.css('::text').extract_first()
    item['text'] = ''
    item['url'] = taga.css('::attr(href)').extract_first()
    item['source'] = source
    item['dtCrawled'] = datetime.datetime.now()
    item['dtCreated'] = ''
    return item
    pass

class SinaSpider(scrapy.Spider):
    source = 'Sina'
    name = source + 'Spider'
    start_urls = [
        'http://finance.sina.com.cn',
        'http://finance.sina.com.cn/stock/',
        ]

    def parse(self, response):
        # find all <a>
        listTaga = []
        try:
            listTaga = listTaga + response.css('div[id="blk_hdline_01"]').css('a')
            listTaga = listTaga + response.css('div[class="m-p1-mb1-list m-list-container"]').css('a')
            listTaga = listTaga + response.css('div[data-client="scroll important"]').css('a')
            listTaga = listTaga + response.css('div[data-sudaclick="blk_yw_zq_01_1"]').css('a')
            listTaga = listTaga + response.css('div[data-sudaclick="blk_yw_zq_01_2"]').css('a')
            listTaga = listTaga + response.css('div[data-sudaclick="blk_yw_zq_01_3"]').css('a')
            listTaga = listTaga + response.css('div[data-sudaclick="blk_yw_zq_01_4"]').css('a')

            listTaga = listTaga + response.css('div[class="hdline"]').css('a')
            listTaga = listTaga + response.css('ul[class="list01"]').css('a')
            listTaga = listTaga + response.css('ul[class="list02"]').css('a')
            listTaga = listTaga + response.css('ul[class="list03"]').css('a')
            listTaga = listTaga + response.css('ul[class="list04"]').css('a')
        except:
            logging.log(logging.ERROR, 'Home page parse error')
            logging.exception(self.source)
            return
        
        # crawl taga
        for taga in listTaga:
            if dirbot.settings.DICT_SWITCH['PARSE_PAGE'] is True:
                full_url = taga.css('::attr(href)').extract_first()
                self.title = taga.css('::text').extract_first()
                yield scrapy.Request(full_url, callback=self.parse_page)
            else:
                item = buildItem(taga, self.source)
                yield item

    def parse_page(self, response):
        if response is None:
            logging.log(logging.ERROR, 'null response')
            return
        
        try:
            title = response.css('h1[id="artibodyTitle"]::text').extract_first()
            dtCreated = response.css('span[class="time-source"]::text').extract_first()
            if dtCreated is None:
                # http://finance.sina.com.cn/zl/stock/20160616/082024822271.shtml
                dtCreated = response.css('span[class="pub_date"]::text').extract_first()
            if dtCreated is None:
                # http://finance.sina.com.cn/fawen/yx/2017-09-01/doc-ifykqmrv6758137.shtml
                dtCreated = response.css('span[class="atc-date"]::text').extract_first()
            # replace nian yue ri in Chinese
            dtCreated = re.sub('[^\d:]+', ' ', dtCreated)
            dtCreated = dateutil.parser.parse(dtCreated + '+8:00')
            text = response.css('div[id="artibody"]').css('::text').extract()
            text = ' '.join(text)
            text = re.sub('[\s\t\n][\s\t\n]+', '', text)
    
            item = News()
            item['title'] = title
            item['text'] = text
            item['url'] = response.url
            item['source'] = self.source
            item['dtCrawled'] = datetime.datetime.now()
            item['dtCreated'] = dtCreated 
            yield item
        except Exception, err:
            logging.exception('FORMAT Problem' + response.url)
            if title is not None:
                logging.log(logging.ERROR, title) 
            if dtCreated is not None:
                logging.log(logging.ERROR, dtCreated)
            # for non-structed page, extract p::text 
            text = response.css('p::text').extract()
            text = ' '.join(text)
            item = News()
            item['title'] = self.title
            item['text'] = text
            item['url'] = response.url
            item['source'] = self.source
            item['dtCrawled'] = datetime.datetime.now()
            item['dtCreated'] = ''
            yield item

	    

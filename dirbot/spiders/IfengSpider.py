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

class IfengSpider(scrapy.Spider):
    source = 'Sina'
    name = source + 'Spider'
    start_urls = [
            'http://finance.ifeng.com',
            'http://finance.ifeng.com/macro/policy/',
            'http://finance.ifeng.com/stock/fhbp/',
            'http://finance.ifeng.com/stock/ssgs/'
            ]
    def parse(self, response):
        # find all <a>
        listTaga = []
        try:
            if response.url == 'http://finance.ifeng.com':
                listTaga = listTaga + response.css('div[class="box_01"]').css('li').css('a')
                listTaga = listTaga + response.css('div[class="box_02"]').css('li').css('a')
                listTaga = listTaga + response.css('div[class="box_03"]').css('li').css('a')
            else:
                listTaga = listTaga + response.css('div[class="box_list"]').css('li').css('h3>a')
        except:
            logging.log(logging.ERROR, 'Home page parse error')
            logging.exception(self.source)
            return
        
        # crawl taga
        for taga in listTaga:
            if dirbot.settings.DICT_SWITCH['PARSE_PAGE'] is True:
                full_url = taga.css('::attr(href)').extract_first().strip()
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
            title = response.css('h1[id="artical_topic"]::text').extract_first()
            dtCreated = response.css('span[class="ss01"]::text').extract_first()
            dtCreated = re.sub('[^\d:]+', ' ', dtCreated)   # replace non digit and colon
            dtCreated = dateutil.parser.parse(dtCreated + '+8:00')
            text = response.css('div[id="main_content"]').css('::text').extract()
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

	    

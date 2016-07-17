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

class SZKXSpider(scrapy.Spider):
    source = 'SZKX'
    name = source + 'Spider'
    start_urls = [
            'http://news.cnstock.com/gdxw/1',
            ]
    def parse(self, response):
        # find all <a>
        listTaga = []
        try:
            listTaga = listTaga + response.css('ul[id="bw-list"]').css('div[class="title"]').css('a')
        except:
            logging.log(logging.ERROR, 'Home page parse error')
            logging.exception(self.source)
            return
        
        # crawl taga
        for taga in listTaga:
            if dirbot.settings.DICT_SWITCH['PARSE_PAGE'] is True:
                full_url = taga.css('::attr(href)').extract_first().strip()
                title = taga.css('::text').extract_first()
                yield scrapy.Request(full_url, callback=self.parse_page, meta={'title': title})
            else:
                item = buildItem(taga, self.source)
                yield item

        # next page
        if dirbot.settings.DICT_SWITCH['SZKX']['HISTORY'] is True:
            strNextPage = u'\u4e0b\u4e00\u9875'
            urlNextPage = response.xpath(u'//a[text()="%s"]/@href'%strNextPage).extract_first()
            if urlNextPage is not None:
                yield scrapy.Request(urlNextPage, callback=self.parse)

    def parse_page(self, response):
        if response is None:
            logging.log(logging.ERROR, 'null response')
            return
        try:
            title = response.css('h1[class="title"]::text').extract_first()
            dtCreated = response.css('span[class="timer"]::text').extract_first()
            dtCreated = re.sub('[^\d:]+', ' ', dtCreated)   # replace non digit and colon
            dtCreated = dateutil.parser.parse(dtCreated + '+8:00')
            text = response.css('div[id="qmt_content_div"]').css('p::text').extract()
            text = ' '.join(text)
    
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
            item['title'] = response.meta['title']
            item['text'] = text
            item['url'] = response.url
            item['source'] = self.source
            item['dtCrawled'] = datetime.datetime.now()
            item['dtCreated'] = ''
            yield item

	    

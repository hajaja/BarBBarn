import scrapy
from dirbot.items import Website, News
import dirbot.settings
import datetime
import logging
import dateutil.parser
import traceback

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

class CNStockSpider(scrapy.Spider):
    source = 'CNStock'
    name = source + 'Spider'
    start_urls = ['http://www.cnstock.com']
    def parse(self, response):
        # find all <a>
        '''
        listTaga = []
        divSelected = response.css('div[class="top-area"]')
        listTaga = listTaga + divSelected.css('h1>a')
        listTaga = listTaga + divSelected.css('h4>a')
        listTaga = listTaga + response.css('div[class="top-list"]').css('a')
        '''
        listTaga = response.css('div[class^="top"]').css('a')
        listTaga = listTaga + response.css('div[class^="box"]').css('a')
        print listTaga

        # crawl taga
        for taga in listTaga:
            if dirbot.settings.DICT_SWITCH['PARSE_PAGE'] is True:
                full_url = taga.css('::attr(href)').extract_first()
                yield scrapy.Request(full_url, callback=self.parse_page)
            else:
                item = buildItem(taga, self.source)
                yield item

    def parse_page(self, response):
        if response is None:
            logging.log(logging.ERROR, 'null response')
            return
        
        try:
            title = response.css('h1[class="title"]::text').extract_first()
            if title is None:
                title = response.css('h1::text').extract_first()
            
            dtCreated = response.css('span[class="timer"]::text').extract_first()
            if dtCreated is None:
                dtCreated = response.css('span[class="time"]::text').extract_first()
            if dtCreated is None:
                # http://zhuanti10.blog.cnstock.com
                dtCreated = response.css('div[class="ll-time"]::text').extract_first()
            if dtCreated is None:
                # http://news.cnstock.com/theme,1562.html
                dtCreated = response.css('p[class="time"]::text').extract_first()
            print dtCreated
            if dtCreated is None:
                print response
            else:
                dtCreated = dateutil.parser.parse(dtCreated + '+8:00')

            text = response.css('div[id="qmt_content_div"]').css('p::text').extract()
            if text is None:
                print response
                text = response.css('p::text').extract()

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
            logging.exception('FORMAT Problem, parse_page')
            logging.log(logging.ERROR, response.url)
            return

	    

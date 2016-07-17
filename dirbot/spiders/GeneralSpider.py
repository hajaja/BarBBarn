import scrapy
from dirbot.items import Website, News
import dirbot.settings
import datetime
import logging
import dateutil.parser
import traceback
import re
import time

class GeneralSpider(scrapy.Spider):
    name = 'GeneralSpider'
    start_urls = [
            'http://finance.sina.com.cn/',
            'http://finance.ifeng.com/',
            'http://finance.qq.com/',
            'http://finance.sohu.com/',
            'http://www.cnstock.com/',
            'http://www.caijing.com.cn/',
            'http://www.jrj.com.cn/',
            'http://www.yicai.com/',
            'http://www.10jqka.com.cn/',
            'http://www.eastmoney.com/',
            ]
    def parse(self, response):
        self.download_delay = 20
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
        
        # crawl taga
        for taga in listTaga:
            full_url = taga.css('::attr(href)').extract_first().strip()
            title = taga.css('::text').extract_first()
            yield scrapy.Request(full_url, callback=self.parse_page, meta={'title': title})
        
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
                #title = response.css('h1[id="artibodyTitle"]::text').extract_first()
                dtCreated = response.css('span[class="time-source"]::text').extract_first()
                if dtCreated is None:
                    # http://finance.sina.com.cn/zl/stock/20160616/082024822271.shtml
                    dtCreated = response.css('span[class="pub_date"]::text').extract_first()
                # replace nian yue ri in Chinese
                dtCreated = re.sub('[^\d:]+', ' ', dtCreated)
                dtCreated = dateutil.parser.parse(dtCreated + '+8:00')
                text = response.css('div[id="artibody"]').css('::text').extract()
                text = ' '.join(text)
                text = re.sub('[\s\t\n][\s\t\n]+', '', text)
            elif source is 'Ifeng':
                #title = response.css('h1[id="artical_topic"]::text').extract_first()
                dtCreated = response.css('span[class="ss01"]::text').extract_first()
                dtCreated = re.sub('[^\d:]+', ' ', dtCreated)   # replace non digit and colon
                dtCreated = dateutil.parser.parse(dtCreated + '+8:00')
                text = response.css('div[id="main_content"]').css('::text').extract()
                text = ' '.join(text)
                text = re.sub('[\s\t\n][\s\t\n]+', '', text)
            elif source is 'QQ':
                dtCreated = response.css('span[class="pubTime article-time"]::text').extract_first()
                dtCreated = re.sub('[^\d:]+', ' ', dtCreated)   # replace non digit and colon
                dtCreated = dateutil.parser.parse(dtCreated + '+8:00')
                text = response.css('div[id="Cnt-Main-Article-QQ"]').css('::text').extract()
                text = ' '.join(text)
                text = re.sub('[\s\t\n][\s\t\n]+', '', text)
            elif source is 'Sohu':
                #title = response.css('h1[id="artical_topic"]::text').extract_first()
                dtCreated = response.css('div[class="time"]::text').extract_first()
                dtCreated = re.sub('[^\d:]+', ' ', dtCreated)   # replace non digit and colon
                dtCreated = dateutil.parser.parse(dtCreated + '+8:00')
                text = response.css('div[itemprop="articleBody"]').css('::text').extract()
                text = ' '.join(text)
                text = re.sub('[\s\t\n][\s\t\n]+', '', text)
            elif source is 'CNStock':
                #title = response.css('h1[class="title"]::text').extract_first()
                if title is None:
                    title = response.css('h1::text').extract_first()
                dtCreated = response.css('span[class="timer"]::text').extract_first()
                if dtCreated is None:
                    dtCreated = response.css('span[class="time"]').extract_first()
                dtCreated = dateutil.parser.parse(dtCreated + '+8:00')
                text = response.css('div[id="qmt_content_div"]').css('p::text').extract()
                text = ' '.join(text)
            elif source is 'Caijing':
                #title = response.css('h1[id="cont_title"]::text').extract_first()
                dtCreated = response.css('span[id="pubtime_baidu"]::text').extract_first()
                dtCreated = re.sub('[^\d:]+', ' ', dtCreated)   # replace non digit and colon
                dtCreated = dateutil.parser.parse(dtCreated + '+8:00')
                text = response.css('div[id="the_content"]').css('::text').extract()
                text = ' '.join(text)
                pass
            elif source is 'JRJ':
                #title = response.css('h1::text').extract_first()
                dtCreated = response.css('p[class="inftop"]>span')[0].css('::text').extract_first()
                dtCreated = re.sub('[^\d:]+', ' ', dtCreated)   # replace non digit and colon
                dtCreated = dateutil.parser.parse(dtCreated + '+8:00')
                text = response.css('div[class="texttit_m1"]').css('::text').extract()
                text = ' '.join(text)
                pass
            elif source is 'CBN':
                dtCreated = response.css('h2>span')[1].css('::text').extract_first()
                dtCreated = re.sub('[^\d:]+', ' ', dtCreated)   # replace non digit and colon
                dtCreated = dateutil.parser.parse(dtCreated + '+8:00')
                text = response.css('div[class="m-text"]').css('::text').extract()
                text = ' '.join(text)
            elif source is 'THS':
                #title = response.css('h1::text').extract_first()
                dtCreated = response.css('span[id="pubtime_baidu"]::text').extract_first()
                dtCreated = re.sub('[^\d:]+', ' ', dtCreated)   # replace non digit and colon
                dtCreated = dateutil.parser.parse(dtCreated + '+8:00')
                text = response.css('div[class="atc_content"]').css('::text').extract()
                text = ' '.join(text)
                pass
            elif source is 'EastMoney':
                #title = response.css('h1::text').extract_first()
                dtCreated = response.css('div[class="Info"]>span')[0].css('::text').extract_first()
                dtCreated = re.sub('[^\d:]+', ' ', dtCreated)   # replace non digit and colon
                dtCreated = dateutil.parser.parse(dtCreated + '+8:00')
                text = response.css('div[class="Body"]').css('::text').extract()
                text = ' '.join(text)
                pass
            else:
                logging.log(logging.INFO, response.url)
                raise Exception('Unknown Source')

        except Exception:
            logging.exception('Exception' + response.url)
            title = response.meta['title']
            dtCreated = ''
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


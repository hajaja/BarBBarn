#encoding=utf8
import scrapy
from dirbot.items import Blog
import dirbot.settings
import datetime
import logging
import dateutil.parser
import traceback
import re
import pdb
import time
import random

class BlogSinaSpider(scrapy.Spider):
    name = 'BlogSinaSpider'
    DELAY_BLOG = 3
    start_urls = [
            #'http://blog.sina.com.cn/s/articlelist_1284139322_0_1.html',   #Cannes
            #'http://blog.sina.com.cn/s/articlelist_1279884602_0_1.html',   #shaminnong
            #'http://blog.sina.com.cn/s/articlelist_2042849783_0_1.html',    #bolaaikong
            #'http://blog.sina.com.cn/s/articlelist_1215172700_0_1.html',    #chanzhongshuochan
            #'http://blog.sina.com.cn/s/articlelist_1364334665_0_1.html',    #yerongtian
            #'http://blog.sina.com.cn/s/articlelist_1278228085_0_1.html',    #xuwenming
            #'http://blog.sina.com.cn/s/articlelist_1282871591_0_1.html',    #huarong
            #'http://blog.sina.com.cn/s/articlelist_1233227211_0_1.html',    #yetan
            'http://blog.sina.com.cn/s/articlelist_1092672395_0_1.html',    #langxianping
            ]

    def parse(self, response):
        listTaga = []
        try:
            listTagaTemp = response.css('div[class="articleCell SG_j_linedot1"]')
            for tagDiv in listTagaTemp:
                item = Blog()
                item['dtCreated'] = dateutil.parser.parse(tagDiv.css('span[class="atc_tm SG_txtc"]::text').extract_first())
                item['url'] = tagDiv.css(u'span[class="atc_title"]>a::attr(href)').extract_first()
            
                full_url = item['url']
                time.sleep(random.random() * self.DELAY_BLOG)
                yield scrapy.Request(full_url, callback=self.parse_page, meta={'item': item})
        except Exception, e:
            logging.log(logging.ERROR, 'Home page parse error')
            print traceback.format_exc()
            pdb.set_trace()
            return
        
        # next page
        strNextPage = u'下一页'
        urlNextPage = response.xpath(u'//a[contains(text(),"%s")]/@href'%strNextPage).extract_first()
        if urlNextPage is not None:
            time.sleep(random.random() * self.DELAY_BLOG)
            yield scrapy.Request(urlNextPage, callback=self.parse)

    def parse_page(self, response):
        self.source = self.parseSource(response)
        if response is None:
            logging.log(logging.ERROR, 'null response')
            return
        try:
            if self.source is 'Sina':
                title = response.css('h2[class="titName SG_txta"]::text').extract_first()
                text = response.css('div[id="sina_keyword_ad_area2"]').css('::text').extract()
                text = '\n'.join(text)
                text = re.sub('[\s\t\n][\s\t\n]+', '', text)
                #author = response.css('h1[id="blogname"]>a::attr(href)').extract_first().split('/')[-1]
                author = 'langxianping'

                item = response.meta['item']
                item['title'] = title
                item['author'] = author
                item['text'] = text
                item['source'] = self.source
                yield item
    
            else:
                logging.log(logging.INFO, response.url)
                raise Exception('Unknown Source')

        except Exception:
            logging.exception('Exception' + response.url)
	    
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


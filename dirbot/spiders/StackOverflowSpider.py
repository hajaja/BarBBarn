import scrapy
from dirbot.items import Website
import logging
class StackOverflowSpider(scrapy.Spider):
    name = 'StackOverflowSpider'
    start_urls = ['http://stackoverflow.com/questions?sort=votes']

    def parse(self, response):
        for href in response.css('div[id^="question-summary"]>div>h3>a::attr(href)'):
            full_url = response.urljoin(href.extract())
            yield scrapy.Request(full_url, callback=self.parse_question)
        logging.log(logging.DEBUG, 'LogFromStackOverflowSpider')

    def parse_question(self, response):
	item = Website()
	item['name'] = response.css('h1 a::text').extract_first()
        item['description'] = response.css('.question .post-text').extract_first()
        item['url'] = response.url
	yield item

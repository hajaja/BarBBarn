import scrapy
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner, CrawlerProcess
from scrapy.utils.log import configure_logging
from dirbot.spiders import DmozSpider, StackOverflowSpider, CNStockSpider, SinaSpider, IfengSpider, SZKXSpider, GeneralSpider, BlogSinaSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import sys
import logging

# for import file from sibling/parent directory
sys.path.append("/home/csdong/dongcs/BarBBarn/dirbot/")

# logging setting
# more on http://doc.scrapy.org/en/latest/topics/logging.html
logging.basicConfig(
        level = logging.DEBUG,
        format = '%(asctime)s [%(name)s] %(levelname)s: %(message)s',
        datefmt = '%m-%d %H:%M:%S',
        filename = 'crawl.log',
        filemode = 'w'
        )

# add spiders
runner = CrawlerRunner()
runner.settings['ITEM_PIPELINES'] = {'dirbot.pipelines.FilterWordsPipeline': 1, 'dirbot.pipelines.MongoDBPipeline':1}
#runner.crawl(DmozSpider.DmozSpider())
#runner.crawl(StackOverflowSpider.StackOverflowSpider())
#runner.crawl(CNStockSpider.CNStockSpider())
runner.crawl(SinaSpider.SinaSpider())
#runner.crawl(IfengSpider.IfengSpider())
#runner.crawl(SZKXSpider.SZKXSpider())
#runner.crawl(GeneralSpider.GeneralSpider())
#runner.crawl(BlogSinaSpider.BlogSinaSpider())

d = runner.join()
d.addBoth(lambda _: reactor.stop())
reactor.run() # the script will block here until all crawling jobs are finished



# Scrapy settings for dirbot project

SPIDER_MODULES = ['dirbot.spiders']
NEWSPIDER_MODULE = 'dirbot.spiders'
DEFAULT_ITEM_CLASS = 'dirbot.items.News'

ITEM_PIPELINES = {'dirbot.pipelines.FilterWordsPipeline': 1, 'dirbot.pipelines.MongoDBPipeline':1}

DICT_SWITCH = {
        'PARSE_PAGE': True,
        'SZKX': {
            'HISTORY': True,
            },
        }

# download frequency
DOWNLOAD_DELAY = 3
CONCURRENT_REQUESTS_PER_DOMAIN = 1
CONCURRENT_REQUESTS_PER_IP = 1
CONCURRENT_REQUESTS = 1
CONCURRENT_REQUESTS_PER_SPIDER = 1
RANDOM_DOWNLOAD_DELAY = False

# middle wares
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': None,
    'dirbot.middlewares.DownloadMiddleware.RotateUserAgentMiddleware': 400,
    }


import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

# remove the comments below for scrapy shell run
# from amazonmws import django_cli
# django_cli.execute()

from amazonmws import settings as amazonmws_settings

# -*- coding: utf-8 -*-

# Scrapy settings for amzn project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

LOG_LEVEL = amazonmws_settings.APP_LOG_LEVEL

BOT_NAME = 'amzn'

SPIDER_MODULES = ['amzn.spiders']
NEWSPIDER_MODULE = 'amzn.spiders'

# disabled duplicate filter since it's filtering out all amzn categories
DUPEFILTER_CLASS = 'amzn.dupefilters.DisabledGlobalDupeFilter'
DUPEFILTER_DEBUG = True

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'amznbot';

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS=16

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY=2
# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN=16
#CONCURRENT_REQUESTS_PER_IP=16

# Disable cookies (enabled by default)
COOKIES_ENABLED=False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED=False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
    # 'amzn.middlewares.CacheAmazonItemMiddleware': 950,
    'amzn.middlewares.RemovedVariationHandleMiddleware': 960, # should not bothered by CacheAmazonItemMiddleware
}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    # 'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
    # 'amzn.middlewares.RandomProxyMiddleware': 100,
    # 'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
    'amzn.middlewares.AmazonItemCrawlControlMiddleware': 50,
    'amzn.middlewares.RandomUserAgentMiddleware': 400,
    'scrapy_crawlera.CrawleraMiddleware': 600,
    'amzn.middlewares.TorProxyMiddleware': 650,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'amzn.pipelines.AmazonItemCachePipeline': 50,
    'amzn.pipelines.ScrapyTaskPipeline': 70,
    'amzn.pipelines.DBPipeline': 100,
    'amzn.pipelines.AmazonToEbayCategoryMapPipeline': 200,
    'amzn.pipelines.EbayItemListingPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
# NOTE: AutoThrottle will honour the standard settings for concurrency and delay
#AUTOTHROTTLE_ENABLED=True
# The initial download delay
#AUTOTHROTTLE_START_DELAY=5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY=60
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG=False
AUTOTHROTTLE_ENABLED = False
DOWNLOAD_TIMEOUT = 600

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED=True
#HTTPCACHE_EXPIRATION_SECS=0
#HTTPCACHE_DIR='httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES=[]
#HTTPCACHE_STORAGE='scrapy.extensions.httpcache.FilesystemCacheStorage'

RETRY_TIMES = amazonmws_settings.APP_HTTP_CONNECT_RETRY_TIMES
# PROXY_LIST = os.path.join(amazonmws_settings.SCRAPER_PATH, 'proxy_list.txt')

# ROBOTSTXT_OBEY = True

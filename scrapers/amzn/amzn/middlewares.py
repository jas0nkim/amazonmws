import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

import re
import random
import base64
import logging
import datetime

from scrapy.exceptions import IgnoreRequest

from amazonmws import settings as amazonmws_settings, utils as amazonmws_utils
from amazonmws.model_managers import *

from amzn.spiders.amazon_pricewatch import AmazonPricewatchSpider


class TorProxyMiddleware(object):
    proxy = None

    def __init__(self, settings):
        self.proxy = 'http://%s:%d' % (amazonmws_settings.APP_HOST, amazonmws_settings.PRIVOXY_LISTENER_PORT)
        amazonmws_utils.renew_tor_connection()
        logging.debug('Tor connection renewed')

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_request(self, request, spider):
        if self._is_enabled_for_request(request, spider):
            request.meta['proxy'] = self.proxy
        return None

    def process_response(self, request, response, spider):
        if not self._is_enabled_for_request(request, spider):
            return response

        if response.status == 503:
            logging.error('Service Unavailable <%s> HTTP status %d - renewing Tor connection' % (request.url, response.status))
            amazonmws_utils.renew_tor_connection()
            logging.debug('Tor connection renewed')
            return request

        # if robot check screen shows up, renew connection
        try:
            if len(response.css('title::text')) > 0:
                title = response.css('title::text')[0].extract().strip().lower()
                if title == 'robot check':
                    logging.error('IP caught by amazon.com <%s> - renewing Tor connection' % request.url)
                    amazonmws_utils.renew_tor_connection()
                    logging.debug('Tor connection renewed')
                    return request
        except AttributeError as e:
            logging.error(str(e))
        return response

    def process_exception(self, request, exception, spider):
        if not self._is_enabled_for_request(request, spider):
            return None

        logging.exception(exception)
        logging.error('Tor Proxy failed <%s> - renewing Tor connection' % request.meta['proxy'])
        amazonmws_utils.renew_tor_connection()
        logging.debug('Tor connection renewed')
        return None

    def _is_enabled_for_request(self, request, spider):
        return 'dont_proxy' not in request.meta and getattr(spider, 'tor_privoxy_enabled', False)


class RandomProxyMiddleware(object):
    def __init__(self, settings):
        self.proxy_list = settings.get('PROXY_LIST')
        fin = open(self.proxy_list)

        self.proxies = {}
        for line in fin.readlines():
            parts = re.match('(\w+:\w+@)?(.+)', line)
            
            # Cut trailing @
            if parts.group(1):
                user_pass = parts.group(1)[:-1]
            else:
                user_pass = ''

            self.proxies['http://%s' % parts.group(2)] = user_pass

        fin.close()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_request(self, request, spider):
        # Don't overwrite with a random one (server-side state for IP)
        if 'proxy' in request.meta:
            return None

        proxy_address = random.choice(self.proxies.keys())
        proxy_user_pass = self.proxies[proxy_address]

        request.meta['proxy'] = proxy_address
        if proxy_user_pass:
            basic_auth = 'Basic ' + base64.encodestring(proxy_user_pass)
            request.headers['Proxy-Authorization'] = basic_auth
        return None

    def process_exception(self, request, exception, spider):
        proxy = request.meta['proxy']
        logging.error('Removing failed proxy <%s>, %d proxies left' % (
                    proxy, len(self.proxies)))
        try:
            self.proxies.remove(proxy)
        except ValueError:
            pass
        return None


class RandomUserAgentMiddleware(object):
    crawlera_enabled = False

    def __init__(self, settings):
        self.ua_list = amazonmws_settings.USER_AGENT_LIST

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_request(self, request, spider):
        if self._is_enabled_for_request(spider):
            ua = random.choice(self.ua_list)
            if ua:
                request.headers.setdefault('User-Agent', ua)
                if self.crawlera_enabled:
                    request.headers['X-Crawlera-UA'] = 'desktop'
        return None

    def _is_enabled_for_request(self, spider):
        self.crawlera_enabled = getattr(spider, 'crawlera_enabled', False)
        return getattr(spider, 'rand_user_agent_enabled', False)


class CachedAmazonItemMiddleware(object):

    def __store_amazon_scrape_tasks(self, task_id, ebay_store_id, asin, parent_asin=None):
        t = AmazonScrapeTaskModelManager.fetch_one(task_id=task_id, ebay_store_id=ebay_store_id, asin=asin)
        if not t:
            AmazonScrapeTaskModelManager.create(
                task_id=task_id,
                ebay_store_id=ebay_store_id,
                asin=asin,
                parent_asin=parent_asin if parent_asin else asin)
        return True


    def process_request(self, request, spider):
        if isinstance(spider, AmazonPricewatchSpider):
            # do NOT use CachedAmazonItemMiddleware for price watch (repricer) spiders
            return None
        if not spider.crawl_cache:
            return None
        asin = amazonmws_utils.extract_asin_from_url(request.url)
        amazon_item = AmazonItemModelManager.fetch_one(asin=asin)
        if amazon_item and amazon_item.updated_at > datetime.datetime.now(tz=amazonmws_utils.get_utc()) - datetime.timedelta(days=3):
            raise IgnoreRequest
        return None

    def process_exception(self, request, exception, spider):
        if isinstance(spider, AmazonPricewatchSpider):
            # do NOT use CachedAmazonItemMiddleware for price watch (repricer) spiders
            return None
        if not spider.crawl_cache:
            return None
        asin = amazonmws_utils.extract_asin_from_url(request.url)
        logging.warning("[ASIN:{}] No crawling. This amazon item has crawled very recently".format(asin))
        if spider.task_id and spider.ebay_store_id:
            amazon_item = AmazonItemModelManager.fetch_one(asin=asin)
            self.__store_amazon_scrape_tasks(task_id=spider.task_id,
                ebay_store_id=spider.ebay_store_id,
                asin=amazon_item.asin,
                parent_asin=amazon_item.parent_asin)
        return None


class RepricingHistoryMiddleware(object):

    def __is_repricable(self, asin, frequency=amazonmws_settings.EBAY_ITEM_DEFAULT_REPRICING_HOUR):
        histories = EbayItemRepricedHistoryModelManager.fetch(parent_asin=asin, updated_at__lt=datetime.datetime.now(tz=amazonmws_utils.get_utc()) - datetime.timedelta(hours=frequency))

        if histories.count() > 0:
            # repriced already
            return False
        return True


    def process_request(self, request, spider):
        if type(spider) != AmazonPricewatchSpider:
            # must exact AmazonPricewatchSpider, not subclass of AmazonPricewatchSpider
            # price watch (repricer) spider ONLY middleware
            return None
        # 1. check popularity - given from spider
        # 2. check repricing history within given time frame
        asin = amazonmws_utils.extract_asin_from_url(request.url)
        hour = amazonmws_settings.EBAY_ITEM_DEFAULT_REPRICING_HOUR
        for data in amazonmws_settings.EBAY_ITEM_POPULARITY_REPRICING_HOURS:
            if data['popularity'] == spider.popularity:
                hour = data['hour']
                break
        if not self.__is_repricable(asin=asin, frequency=hour):
            raise IgnoreRequest
        return None

    def process_exception(self, request, exception, spider):
        asin = amazonmws_utils.extract_asin_from_url(request.url)
        logging.warning("[ASIN:{}] No crawling. Related ebay items have repriced recently".format(asin))
        return None

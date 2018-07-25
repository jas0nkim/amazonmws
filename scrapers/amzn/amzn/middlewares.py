import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

import re
import random
import base64
import logging
import datetime
import time
import urllib

from scrapy.http import HtmlResponse
from scrapy.selector import Selector
from scrapy.exceptions import IgnoreRequest

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.proxy import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from amazonmws import django_cli
django_cli.execute()

from amazonmws import settings as amazonmws_settings, utils as amazonmws_utils
from amazonmws.model_managers import *

from amzn.spiders.amazon_base import AmazonBaseSpider
from amzn.spiders.amazon_asin import AmazonAsinSpider
from amzn.spiders.amazon_pricewatch import AmazonPricewatchSpider
from amzn.spiders.aliexpress.store import AliexpressStoreSpider
from amzn.items import AmazonItem

""" Downloader Middlewares
"""

""" DEPRECATED - TorProxyMiddleware
"""
class TorProxyMiddleware(object):
    proxy = None

    def __init__(self, settings):
        self.proxy = 'http://%s:%d' % (amazonmws_settings.APP_HOST, amazonmws_settings.PRIVOXY_LISTENER_PORT)
        # amazonmws_utils.renew_tor_connection()
        # logging.debug('Tor connection renewed')

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


class AmazonItemCrawlControlMiddleware(object):

    def process_request(self, request, spider):
        if not isinstance(spider, AmazonBaseSpider) and not isinstance(spider, AmazonAsinSpider):
            return None
        if hasattr(spider, 'force_crawl') and spider.force_crawl == True:
            return None
        if type(spider) == AmazonPricewatchSpider:
            return self.__handle_pricewatch_spider_request(request=request, spider=spider)
        return self.__handle_amazon_item_spider_request(request=request, spider=spider)

    def __handle_amazon_item_spider_request(self, request, spider):
        asin = ''
        try:
            asin = amazonmws_utils.extract_asin_from_url(request.url)
            cached_data = AmazonItemModelManager.fetch_one(asin=asin, updated_at__gt=datetime.datetime.now(tz=amazonmws_utils.get_utc()) - datetime.timedelta(hours=amazonmws_settings.AMAZON_ITEM_DEFAULT_HTML_CACHING_SCHEDULE))
            if cached_data:
                # build response via cached html page
                return HtmlResponse(url=request.url,
                    request=request,
                    flags=[ 'cached_amazon_item', ])
            return None
        except Exception as e:
            logging.error("[ASIN:{}] Failed using AmazonItemCrawlControlMiddleware - {}".format(asin, str(e)))
            return None
        return None

    def __handle_pricewatch_spider_request(self, request, spider):
        asin = ''
        try:
            asin = amazonmws_utils.extract_asin_from_url(request.url)
            hour = amazonmws_settings.AMAZON_ITEM_DEFAULT_HTML_CACHING_SCHEDULE
            for data in amazonmws_settings.AMAZON_ITEM_HTML_CACHING_SCHEDULES:
                try:
                    if data['popularity'] == spider.popularity:
                        hour = data['hour']
                        break
                except Exception:
                    continue
            cached_data = AmazonItemModelManager.fetch_one(asin=asin, updated_at__gt=datetime.datetime.now(tz=amazonmws_utils.get_utc()) - datetime.timedelta(hours=hour))
            if cached_data:
                # build response via cached html page
                return HtmlResponse(url=request.url,
                    request=request,
                    flags=[ 'cached_amazon_item', ])
            return None
        except Exception as e:
            logging.error("[ASIN:{}] Failed using AmazonItemCrawlControlMiddleware - {}".format(asin, str(e)))
            return None
        return None


# deprecated middleware, but KEEP it for a reference
# 
class AliexpressStoreScrapeMiddleware(object):

    __driver = None
    __store_id = None

    def __init_webdriver(self, crawlera_enabled=False):
        try:
            if crawlera_enabled:
                service_args = [ '--ssl-protocol=any', ]
                self.__driver = webdriver.PhantomJS(service_args=service_args)
            else:
                self.__driver = webdriver.PhantomJS()
        except Exception as e:
            raise e

    def __quit_webdriver(self):
        try:
            if self.__driver:
                self.__driver.quit()
        except Exception as e:
            raise e

    def __parse_store(self, crawlera_enabled=False):
        try:
            if crawlera_enabled:
                # https request
                response = self.__driver.get('http://{user}:@{host}:{port}/fetch?url={url}'.format(
                    user=amazonmws_settings.APP_CRAWLERA_API_KEY, 
                    host=amazonmws_settings.APP_CRAWLERA_HOST,
                    port=amazonmws_settings.APP_CRAWLERA_PORT,
                    url=urllib.quote_plus(amazonmws_settings.ALIEXPRESS_STORE_LINK_FORMAT.format(
                        alxstoreid=self.__store_id))))
            else:
                response = self.__driver.get(amazonmws_settings.ALIEXPRESS_STORE_LINK_FORMAT.format(alxstoreid=self.__store_id))

            self.__driver.save_screenshot('/tmp/selenium_phantomjs_ss-{storeid}-{ts}.png'.format(storeid=self.__store_id, ts=time.time()))

            if response and 'success' in response and response['success'] == 0:
                logging.error("[ALXSTOREID:{}] Failed to load aliexpress store".format(self.__store_id))
                return None
            
            scrapy_selector = Selector(text=self.__driver.page_source)

            store_id = self.__store_id
            store_name = self.__extract_store_name(scrapy_selector=scrapy_selector)
            store_location = self.__extract_store_location(scrapy_selector=scrapy_selector)
            store_opened_since = self.__extract_store_opened_since(scrapy_selector=scrapy_selector)
            feedback_score = self.__extract_feedback_score(scrapy_selector=scrapy_selector)
            feedback_percentage = self.__extract_feedback_percentage(scrapy_selector=scrapy_selector)
            itemasdescribed_rating = self.__extract_itemasdescribed_rating()
            communication_rating = self.__extract_communication_rating()
            shippingspeed_rating = self.__extract_shippingspeed_rating()
            deliveryguarantee_days = self.__extract_deliveryguarantee_days()
            return_policy = self.__extract_return_policy()
            is_topratedseller = self.__extract_is_topratedseller()
            has_buyerprotection = self.__extract_has_buyerprotection()

            print(str({
                'store_id': store_id,
                'store_name': store_name,
                'store_location': store_location,
                'store_opened_since': store_opened_since,
                'feedback_score': feedback_score,
                'feedback_percentage': feedback_percentage,
                'itemasdescribed_rating': itemasdescribed_rating,
                'communication_rating': communication_rating,
                'shippingspeed_rating': shippingspeed_rating,
                'deliveryguarantee_days': deliveryguarantee_days,
                'return_policy': return_policy,
                'is_topratedseller': is_topratedseller,
                'has_buyerprotection': has_buyerprotection,
            }))

        except Exception as e:
            # self.__driver.save_screenshot('/tmp/selenium_phantomjs_ss-{storeid}-{ts}.png'.format(storeid=self.__store_id, ts=time.time()))
            raise e

    def __extract_store_name(self, scrapy_selector):
        try:
            return self.__driver.find_element_by_css_selector('span.shop-name a').text.strip()
        except Exception as e:
            logger.error('[ALXSTOREID:{}] error on parsing store name - {}'.format(self.__store_id, str(e)))
            return None

    def __extract_store_location(self, scrapy_selector):
        try:
            store_location_element = scrapy_selector.css('.store-info-header .store-location')
            if len(store_location_element) < 1:
                logger.error('[ALXSTOREID:{}] no location element found'.format(self.__store_id))
                return None
            return ' '.join(store_location_element.css('::text')[0].extract().strip().split())
        except Exception as e:
            logger.error('[ALXSTOREID:{}] error on parsing store location - {}'.format(self.__store_id, str(e)))
            return None

    def __extract_store_opened_since(self, scrapy_selector):
        try:
            store_time_element = scrapy_selector.css('.store-info-header .store-time em')
            if len(store_time_element) < 1:
                logger.error('[ALXSTOREID:{}] no time element found'.format(self.__store_id))
                return None
            return store_time_element.css('::text')[0].extract().strip()
        except Exception as e:
            logger.error('[ALXSTOREID:{}] error on parsing store opened since - {}'.format(self.__store_id, str(e)))
            return None

    def __extract_feedback_score(self, scrapy_selector):
        try:
            wait = WebDriverWait(self.__driver, amazonmws_settings.APP_DEFAULT_WEBDRIVERWAIT_SEC)
            feedback_score_element = wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'span.rank-num'))
            )
            if not feedback_score_element:
                logger.error('[ALXSTOREID:{}] no feedback score element found'.format(self.__store_id))
                return None
            return feedback_score_element.text.strip()
        except TimeoutException as e:
            logger.error('[ALXSTOREID:{}] timedout on parsing feedback score - {}'.format(self.__store_id, str(e)))
        except Exception as e:
            logger.error('[ALXSTOREID:{}] error on parsing feedback score - {}'.format(self.__store_id, str(e)))
            return None

    def __extract_feedback_percentage(self, scrapy_selector):
        try:
            wait = WebDriverWait(self.__driver, amazonmws_settings.APP_DEFAULT_WEBDRIVERWAIT_SEC)
            feedback_percentage_element = wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'span.positive-percent'))
            )
            if not feedback_percentage_element:
                logger.error('[ALXSTOREID:{}] no feedback percentage element found'.format(self.__store_id))
                return None
            return feedback_percentage_element.text.strip().rstrip('%')
        except TimeoutException as e:
            logger.error('[ALXSTOREID:{}] timedout on parsing feedback percentage - {}'.format(self.__store_id, str(e)))
        except Exception as e:
            logger.error('[ALXSTOREID:{}] error on parsing feedback percentage - {}'.format(self.__store_id, str(e)))
            return None

    def __extract_itemasdescribed_rating(self):
        pass

    def __extract_communication_rating(self):
        pass

    def __extract_shippingspeed_rating(self):
        pass

    def __extract_deliveryguarantee_days(self):
        pass

    def __extract_return_policy(self):
        pass

    def __extract_is_topratedseller(self):
        pass

    def __extract_has_buyerprotection(self):
        pass

    def process_request(self, request, spider):
        if not isinstance(spider, AliexpressStoreSpider):
            return None
        if 'storeid' not in request.meta or not request.meta['storeid']:
            raise IgnoreRequest
        try:
            self.__store_id = request.meta['storeid']
            self.__init_webdriver(crawlera_enabled=getattr(spider, 'crawlera_enabled', False))
            self.__parse_store(crawlera_enabled=getattr(spider, 'crawlera_enabled', False))
            self.__quit_webdriver()
        except Exception as e:
            logging.error("[ALXSTOREID:{}] Failed parsing aliexpress store - {}".format(request.meta['storeid'], str(e)))
        # skip scrapy for all aliexpress store requests
        raise IgnoreRequest


""" Spider Middlewares
"""

# deprecated middleware, but KEEP it for a reference
# 
# class CacheAmazonItemMiddleware(object):
# 
#     def process_spider_output(self, response, result, spider):
#         if not isinstance(spider, AmazonBaseSpider) and not isinstance(spider, AmazonAsinSpider):
#             return result
#         try:
#             asin = amazonmws_utils.extract_asin_from_url(response.request.url)
#         except Exception as e:
#             logging.error("Unable to extract ASIN from url - {}".format(str(e)))
#             return result
#         if 'cached_amazon_item' in response.flags:
#             # this response has been generated by cache. skip
#             logging.info("[ASIN:{}] Cached Amazon Item Response. Skip Caching".format(asin))
#             return result
#         # cache html
#         try:
#             page = AmazonItemCachedHtmlPageModelManager.fetch_one(asin=asin) # deprecated class
#             if page:
#                 # update
#                 AmazonItemCachedHtmlPageModelManager.update(page=page, # deprecated class
#                     request_url=response.request.url,
#                     response_url=response.url,
#                     body=response.body)
#             else:
#                 # create
#                 AmazonItemCachedHtmlPageModelManager.create(asin=asin, # deprecated class
#                     request_url=response.request.url,
#                     response_url=response.url,
#                     body=response.body)
#         except Exception as e:
#             logging.error("[ASIN:{}] Failed to cache amazon item html page - {}".format(asin, str(e)))
#         return result

class RemovedVariationHandleMiddleware(object):

    def __handle_removed_variations(self, result, spider):
        for _r in result:
            if isinstance(_r, AmazonItem):
                if not hasattr(spider, '_scraped_parent_asins_cache'):
                    spider._scraped_parent_asins_cache = {}
                parent_asin = AmazonItemModelManager.find_parent_asin(asin=_r.get('asin'))
                if parent_asin and parent_asin not in spider._scraped_parent_asins_cache:
                    try:
                        spider._scraped_parent_asins_cache[parent_asin] = True
                        # compare variations from db and scraped item
                        scraped_variation_asins = _r.get('variation_asins', [])
                        stored_variation_asins = AmazonItemModelManager.fetch_its_variation_asins(parent_asin=parent_asin, updated_at__lt=datetime.datetime.now(tz=amazonmws_utils.get_utc()) - datetime.timedelta(days=amazonmws_settings.AMAZON_ITEM_DELETE_NEVER_UPDATED))
                        removed_variation_asins = set(stored_variation_asins) - set(scraped_variation_asins)
                        if len(removed_variation_asins) > 0:
                            for removed_asin in removed_variation_asins:
                                removed_item = AmazonItem()
                                removed_item['asin'] = removed_asin
                                removed_item['status'] = False
                                yield removed_item
                    except Exception as e:
                        logging.error("Failed on RemovedVariationHandleMiddleware - {}".format(str(e)))
            yield _r

    def process_spider_output(self, response, result, spider):
        if not isinstance(spider, AmazonBaseSpider) and not isinstance(spider, AmazonAsinSpider):
            return result
        try:
            return self.__handle_removed_variations(result, spider)
        except Exception as e:
            logging.error("RemovedVariationHandleMiddleware - {}".format(str(e)))
        return result

import sys, os

sys.path.append('%s/../../' % os.path.dirname(__file__))

import datetime
import urllib
import uuid
import json

from selenium import webdriver

from storm.exceptions import StormError

from ebaysdk.trading import Connection as Trading
from ebaysdk.exception import ConnectionError

from amazonmws import settings
from amazonmws.models import StormStore, AmazonItem, AmazonItemPicture, Scraper, ScraperAmazonItem, EbayItem, EbayListingError, ItemStatusHistory, Task
from amazonmws.spiders.amazon_item_detail_page import AmazonItemDetailPageSpider
from amazonmws.ebaystore.listing import OnError
from amazonmws.loggers import GrayLogger as logger, StaticFieldFilter, get_logger_name

class ActiveAmazonItemMonitor(object):

    amazon_item = None
    ebay_item = None

    driver = None
    page_opened = True

    TASK_ID = Task.ebay_task_monitoring_status_changes

    def __init__(self, amazon_item):
        self.amazon_item = amazon_item
        self.ebay_item = self.__get_ebay_item()
        self.driver = webdriver.PhantomJS()
        logger.addFilter(StaticFieldFilter(get_logger_name(), Task.get_name(self.TASK_ID)))
        # logger.info("[" + basename(__file__) + "] " + "ASIN-PRICE list")

    def __del__(self):
        self.__quit()

    def __quit(self):
        if self.driver:
            self.driver.quit()

        self.page_opened = False

    def __get_ebay_item(self):
        try:
            ebay_item = StormStore.find(EbayItem, EbayItem.amazon_item_id == self.amazon_item.id).one()

            if ebay_item:
                return ebay_item

            return None

        except StormError:
            return None

    def run(self):
        """ - check link (asin) still available
            - check still FBA
            - [TODO] check out of stock
        """

        logger.info("[ASIN: " + self.amazon_item.asin + "] " + "start mornitoring status")

        has_status_updated = False

        # 1. check link (asin) still available
        amazon_item_url = settings.AMAZON_ITEM_LINK_PREFIX + self.amazon_item.asin
        http_code = urllib.urlopen(amazon_item_url).getcode()

        if http_code != 200:
            self.__inactive_item()
            logger.info("[ASIN: " + self.amazon_item.asin + "] " + "link " + amazon_item_url + " not available (" + str(http_code) + ")")
            self.__quit()
            has_status_updated = True
            return True

        self.driver.get(amazon_item_url)

        # 2. check still FBA
        is_fba = AmazonItemDetailPageSpider.is_FBA(self.driver)

        if not is_fba:
            self.__inactive_item()
            logger.info("[ASIN: " + self.amazon_item.asin + "] " +  "not FBA")
            self.__quit()
            has_status_updated = True
            return True

        # TODO: 3. check out of stock

        if not has_status_updated:
            logger.info("[ASIN: " + self.amazon_item.asin + "] " + "status not changed: " + str(self.amazon_item.status))

        self.__quit()
        return True

    def __inactive_item(self):
        if self.ebay_item and self.ebay_item.status != EbayItem.STATUS_INACTIVE:
            ended = self.__end_ebay_item('NotAvailable')
            if ended:
                self.__update_status(AmazonItem.STATUS_INACTIVE, EbayItem.STATUS_INACTIVE)

        self.__update_status(AmazonItem.STATUS_INACTIVE)


    def __generate_ebay_end_item_obj(self, reason_code):
        item = settings.EBAY_END_ITEM_TEMPLATE
        item['MessageID'] = uuid.uuid4()
        item['ItemID'] = self.ebay_item.ebid
        item['EndingReason'] = reason_code
        return item

    def __end_ebay_item(self, reason_code):
        ret = False

        item_obj = self.__generate_ebay_end_item_obj(reason_code)

        try:
            api = Trading(debug=True, warnings=True, domain=settings.EBAY_TRADING_API_DOMAIN)
            api.execute('EndItem', item_obj)

            if api.response.content:
                data = json.loads(api.response.json())

                # print json.dumps(data, indent=4, sort_keys=True)

                if ('ack' in data and data['ack'] == "Success") or ('Ack' in data and data['Ack'] == "Success"):
                    ret = True

                else:
                    self.__log_on_error(unicode(api.response.json()), u'EndItem')

        except ConnectionError, e:
            self.__log_on_error(e, unicode(e.response.dict()), u'EndItem')

        return ret

    def __update_status(self, am_status=None, eb_status=None):

        if am_status == None and eb_status == None:
            logger.error("No amazon status nor ebay status passed")
            return False

        try:
            if am_status != None:
                self.amazon_item.status = am_status
                self.amazon_item.updated_at = datetime.datetime.now()
                StormStore.add(self.amazon_item)

            if self.ebay_item and eb_status != None:
                self.ebay_item.status = eb_status
                self.ebay_item.updated_at = datetime.datetime.now()
                StormStore.add(self.ebay_item)
            
            # log into item_status_history table
            status_history = ItemStatusHistory()
            status_history.amazon_item_id = self.amazon_item.id
            status_history.asin = self.amazon_item.asin
            status_history.am_status = self.amazon_item.status
            if self.ebay_item:
                status_history.ebay_item_id = self.ebay_item.id
                status_history.ebid = self.ebay_item.ebid
                status_history.eb_status = self.ebay_item.status
            status_history.created_at = datetime.datetime.now()
            status_history.updated_at = datetime.datetime.now()                    
            StormStore.add(status_history)

            StormStore.commit()
            return True

        except StormError, e:
            logger.exception("[ASIN: " + self.amazon_item.asin + "] " + "AmazonItem / EbayItem db status update error")
            StormStore.rollback()
            return False

    def __log_on_error(self, e, reason, related_ebay_api=u''):
        OnError(e, self.amazon_item,
            EbayListingError.TYPE_ERROR_ON_END,
            reason,
            related_ebay_api,
            self.ebay_item)


if __name__ == "__main__":
    
    active_amazon_items = StormStore.find(AmazonItem, AmazonItem.status == AmazonItem.STATUS_ACTIVE)

    if active_amazon_items.count() > 0:
        for amazon_item in active_amazon_items:
            monitor = ActiveAmazonItemMonitor(amazon_item)
            monitor.run()

            while monitor.page_opened:
                if not monitor.page_opened:
                    break

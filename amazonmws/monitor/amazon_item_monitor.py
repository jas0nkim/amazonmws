import sys, os

sys.path.append('%s/../../' % os.path.dirname(__file__))

import datetime
import uuid
import json

from selenium import webdriver

from storm.exceptions import StormError

from ebaysdk.trading import Connection as Trading
from ebaysdk.exception import ConnectionError

from amazonmws import settings
from amazonmws.models import StormStore, AmazonItem, AmazonItemPicture, Scraper, ScraperAmazonItem, EbayItem, EbayListingError, ItemPriceHistory, ItemStatusHistory, Task
from amazonmws.spiders.amazon_item_detail_page import AmazonItemDetailPageSpider, AmazonItemDetailPageSpiderException
from amazonmws.ebaystore.listing import OnError, calculate_profitable_price
from amazonmws.loggers import GrayLogger as logger, StaticFieldFilter, get_logger_name


class AmazonItemMonitor(object):

    amazon_item = None
    ebay_item = None

    driver = None

    page_opened = True
    status_updated = False
    price_updated = False

    TASK_ID = Task.ebay_task_monitoring_amazon_items

    def __init__(self, amazon_item):
        self.amazon_item = amazon_item
        self.ebay_item = self.__get_ebay_item()
        self.driver = webdriver.PhantomJS()
        logger.addFilter(StaticFieldFilter(get_logger_name(), Task.get_name(self.TASK_ID)))

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

    def __check_and_get_changed_price_on_item_screen(self):
        price = None
        try:
            price = AmazonItemDetailPageSpider.get_price(self.driver)

        except AmazonItemDetailPageSpiderException:
            logger.exception("[ASIN: " + self.amazon_item.asin + "] " + "No price element can found")

        if price == self.amazon_item.price:
            return False

        else:
            return price

    def run(self):
        """ - check is still FBA
            - check is price still the same
            - check is out of stock
        """

        logger.info("[ASIN: " + self.amazon_item.asin + "] " + "start mornitoring...")

        amazon_item_url = settings.AMAZON_ITEM_LINK_PREFIX + self.amazon_item.asin
        self.driver.get(amazon_item_url)

        # 1. is FBA - on the item detail screen
        is_fba_on_item_screen = AmazonItemDetailPageSpider.is_FBA(self.driver)

        # 2. price still the same
        price_changed = self.__check_and_get_changed_price_on_item_screen()

        if is_fba_on_item_screen and price_changed == False:
            self.__quit()
            return True
        
        else:
            fba_price_from_other_seller = AmazonItemDetailPageSpider.get_fba_item_price_from_other_amazon_sellers(self.driver)

            if not fba_price_from_other_seller: # no longer fba item
                self.__inactive_item()
                logger.info("[ASIN: " + self.amazon_item.asin + "] " +  "not FBA")
                self.__quit()
                self.status_updated = True
                return True

            elif fba_price_from_other_seller != self.amazon_item.price: # price changed - update
                self.__update_price(fba_price_from_other_seller)
                self.__quit()
                self.price_updated = True
                return True

        # TODO: 3. check out of stock

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
                    self.__log_on_error(unicode(api.response.json()), EbayListingError.TYPE_ERROR_ON_END, u'EndItem')

        except ConnectionError, e:
            self.__log_on_error(e, unicode(e.response.dict()), EbayListingError.TYPE_ERROR_ON_END, u'EndItem')

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

    def __update_price(self, amazon_price):
        if self.ebay_item:
            ebay_price = calculate_profitable_price(amazon_price)
            revised = self.__revise_ebay_item(ebay_price)

            if revised:
                try:
                    # update amazon_items table
                    self.amazon_item.price = amazon_price
                    StormStore.add(self.amazon_item)

                    # update ebay_items table
                    self.ebay_item.eb_price = ebay_price
                    StormStore.add(self.ebay_item)
                    
                    # log into item_price_history table
                    price_history = ItemPriceHistory()
                    price_history.amazon_item_id = self.amazon_item.id
                    price_history.asin = self.amazon_item.asin
                    price_history.ebay_item_id = self.ebay_item.id
                    price_history.ebid = self.ebay_item.ebid
                    price_history.am_price = self.amazon_item.price
                    price_history.eb_price = self.ebay_item.eb_price
                    price_history.created_at = datetime.datetime.now()
                    price_history.updated_at = datetime.datetime.now()                    
                    StormStore.add(price_history)

                    StormStore.commit()

                    logger.info("[ASIN: " + self.amazon_item.asin + "] " + "PRICE UPDATED both amazon_item: $" + str(amazon_price) + ", and ebay_item: $" + str(ebay_price))

                except StormError, e:
                    self.__log_on_error(e, u'Price has been revised at ebay, but error occurred updating new prices in amazon_items and ebay_items tables')
        else:
            try:
                # update amazon_items table
                self.amazon_item.price = amazon_price
                StormStore.add(self.amazon_item)

                # log into item_price_history table
                price_history = ItemPriceHistory()
                price_history.amazon_item_id = self.amazon_item.id
                price_history.asin = self.amazon_item.asin
                price_history.am_price = self.amazon_item.price
                price_history.created_at = datetime.datetime.now()
                price_history.updated_at = datetime.datetime.now()
                StormStore.add(price_history)

                StormStore.commit()

                logger.info("[ASIN: " + self.amazon_item.asin + "] " + "PRICE UPDATED only at amazon_item: $" + str(amazon_price))

            except StormError, e:
                self.__log_on_error(e, u'Error occurred updating new prices in amazon_items table - item which has not listed on ebay yet')

    def __revise_ebay_item(self, new_price):

        ret = False

        item_obj = AmazonItemMonitor.generate_ebay_revise_inventory_status_obj(self.ebay_item, new_price)

        try:
            api = Trading(debug=True, warnings=True, domain=settings.EBAY_TRADING_API_DOMAIN)
            api.execute('ReviseInventoryStatus', item_obj)

            if api.response.content:
                data = json.loads(api.response.json())

                # print json.dumps(data, indent=4, sort_keys=True)

                if ('ack' in data and data['ack'] == "Success") or ('Ack' in data and data['Ack'] == "Success"):
                    ret = True

                else:
                    self.__log_on_error(unicode(api.response.json()), EbayListingError.TYPE_ERROR_ON_REVISE_PRICE, u'ReviseInventoryStatus')

        except ConnectionError, e:
            self.__log_on_error(e, unicode(e.response.dict()), EbayListingError.TYPE_ERROR_ON_REVISE_PRICE, u'ReviseInventoryStatus')

        return ret

    @staticmethod
    def generate_ebay_revise_inventory_status_obj(ebay_item, price=None, quantity=None):
        if price == None and quantity == None:
            return None

        item = settings.EBAY_REVISE_INVENTORY_STATUS_TEMPLATE
        item['MessageID'] = uuid.uuid4()
        item['InventoryStatus']['ItemID'] = ebay_item.ebid
        
        if quantity != None:
            item['InventoryStatus']['Quantity'] = quantity
        else:
            item['InventoryStatus'].pop("Quantity", None)

        if price != None:
            item['InventoryStatus']['StartPrice'] = price
        else:
            item['InventoryStatus'].pop("StartPrice", None)

        return item

    def __log_on_error(self, e, type, reason, related_ebay_api=u''):
        OnError(e, self.amazon_item,
            type,
            reason,
            related_ebay_api,
            self.ebay_item)


if __name__ == "__main__":
    
    active_amazon_items = StormStore.find(AmazonItem, AmazonItem.status == AmazonItem.STATUS_ACTIVE)
    num_updated = 0

    if active_amazon_items.count() > 0:
        for amazon_item in active_amazon_items:
            monitor = AmazonItemMonitor(amazon_item)
            monitor.run()

            while monitor.page_opened:
                if not monitor.page_opened:
                    if monitor.status_updated:
                        logger.info("[ASIN: " + amazon_item.asin + "] " + "status changed: " + str(amazon_item.status))
                        num_updated += 1
                        break

                    if monitor.price_updated:
                        logger.info("[ASIN: " + amazon_item.asin + "] " + "price changed: " + str(amazon_item.price))
                        num_updated += 1
                        break
                    break
        
        logger.info("Number of amazon/ebay item status updated: " + str(num_updated) + " items")

        
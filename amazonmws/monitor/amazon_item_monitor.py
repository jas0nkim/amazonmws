import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

import datetime
import uuid
import json
import re

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException

from storm.exceptions import StormError

from ebaysdk.trading import Connection as Trading
from ebaysdk.exception import ConnectionError

import RAKE

from amazonmws import settings, utils
from amazonmws.models import StormStore, AmazonItem, AmazonItemPicture, Scraper, EbayItem, ItemPriceHistory, ItemStatusHistory, Task, EbayStore, LookupAmazonItem, Lookup, LookupOwnership
from amazonmws.spiders.amazon_item_detail_page import AmazonItemDetailPageSpider, AmazonItemDetailPageSpiderException
from amazonmws.spiders.amazon_item_offer_listing_page import AmazonItemOfferListingPageSpider, AmazonItemOfferListingPageSpiderException
from amazonmws.ebaystore.listing import ListingHandler
from amazonmws.errors import record_trade_api_error
from amazonmws.loggers import GrayLogger as logger, StaticFieldFilter, get_logger_name
from amazonmws.ebayapi.request_objects import generate_revise_inventory_status_obj


class AmazonItemMonitor(object):
    ebay_store = None
    amazon_item = None
    ebay_item = None

    driver = None

    status_updated = False
    price_updated = False

    TASK_ID = Task.ebay_task_monitoring_amazon_items

    def __init__(self, ebay_store, amazon_item):
        self.ebay_store = ebay_store
        self.amazon_item = amazon_item
        self.ebay_item = self.__get_ebay_item()
        self.driver = webdriver.PhantomJS()
        logger.addFilter(StaticFieldFilter(get_logger_name(), Task.get_name(self.TASK_ID)))

    def __del__(self):
        self.__quit()

    def __quit(self):
        if self.driver:
            self.driver.quit()

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
            logger.exception("[" + self.ebay_store.username + "][ASIN: " + self.amazon_item.asin + "] " + "No price element can found")

        if price == self.amazon_item.price:
            return False

        else:
            return price

    def __apply_quickpatch(self):
        """TEMP PATCH
            - update amazon_items.category, amazon_items.ebay_category_id
        """
        category = None
        ebay_category_id = None

        # category
        breadcrumbs = None
        try:
            breadcrumbs = self.driver.find_element_by_css_selector('#wayfinding-breadcrumbs_feature_div > ul')

        except NoSuchElementException:
            logger.exception("[ASIN: " + self.amazon_item.asin + "] " + "No breadcrumbs element")
        
        except StaleElementReferenceException, e:
            logger.exception(e)

        if breadcrumbs != None:
            try:
                categories = []
                category_seq = breadcrumbs.find_elements_by_css_selector('li:not(.a-breadcrumb-divider) > span > a')
                if len(category_seq) > 0:
                    for category in category_seq:
                        categories.append(category.text.strip())
                    category = ' : '.join(categories)

            except NoSuchElementException:
                logger.exception("[ASIN: " + self.amazon_item.asin + "] " + "No breadcrumb category elements")
            
            except StaleElementReferenceException, e:
                logger.exception(e)

        # ebay_category_id
        ebay_category_id = None
        if not self.amazon_item.ebay_category_id or self.amazon_item.ebay_category_id == "":
            # RAKE
            Rake = RAKE.Rake(os.path.join(settings.APP_PATH, 'rake', 'stoplists', 'SmartStoplist.txt'));
            # search with category
            if category != None:
                keywords = Rake.run(re.sub(r'([^\s\w]|_)+', ' ', category));
                if len(keywords) > 0:
                    ebay_category_id = utils.find_ebay_category_id(keywords[0][0], self.amazon_item.asin)
            if ebay_category_id < 0:
                # search with title
                keywords = Rake.run(re.sub(r'([^\s\w]|_)+', ' ', self.amazon_item.title));
                if len(keywords) > 0:
                    ebay_category_id = utils.find_ebay_category_id(keywords[0][0], self.amazon_item.asin)
                if ebay_category_id < 0:
                    logger.error("[ASIN: " + self.amazon_item.asin + "] " + "No ebay category found")
                    ebay_category_id = None

        if not category and not ebay_category_id:
            return False

        try:
            if category:
                self.amazon_item.category = category
            if ebay_category_id:
                self.amazon_item.ebay_category_id = ebay_category_id

            StormStore.add(self.amazon_item)
            StormStore.commit()

        except StormError, e:
            logger.exception("[ASIN: " + self.amazon_item.asin + "] " + "AmazonItem db update error")
            StormStore.rollback()
            return False
        
        return True

    def run(self):
        """ - check is still FBA
            - check is price still the same
            - check is out of stock
        """

        logger.info("[" + self.ebay_store.username + "][ASIN: " + self.amazon_item.asin + "] " + "start mornitoring...")

        amazon_item_url = settings.AMAZON_ITEM_LINK_FORMAT % self.amazon_item.asin
        self.driver.get(amazon_item_url)

        # quick patch
        # - update amazon_items.category, amazon_items.ebay_category_id
        self.__apply_quickpatch()

        # check status
        #   - is FBA
        is_fba_on_item_screen = AmazonItemDetailPageSpider.is_FBA(self.driver)

        if not is_fba_on_item_screen:
            try:
                offer_listing = AmazonItemOfferListingPageSpider(self.amazon_item.asin, self.TASK_ID)
                offer_listing.load()

            except AmazonItemOfferListingPageSpiderException, e:
                logger.exception(e)

            finally:
                if not offer_listing.is_fba or offer_listing.best_fba_price != None: # no longer fba item
                    if self.amazon_item.status != AmazonItem.STATUS_INACTIVE:                    
                        self.__inactive_item()
                        self.status_updated = True
                        logger.info("[" + self.ebay_store.username + "][ASIN: " + self.amazon_item.asin + "] " +  "not FBA any more")
                    else:
                        logger.info("[" + self.ebay_store.username + "][ASIN: " + self.amazon_item.asin + "] " +  "still not FBA")

                # TODO
                # # 2. check enough stock available - must check from AmazonItemOfferListingPageSpider
                # has_enough_stock = AmazonItemOfferListingPageSpider.has_enough_stock(self.driver)

                # if not has_enough_stock:
                #     self.__oos_item()
                #     self.status_updated = True
                #     logger.info("[ASIN: " + self.amazon_item.asin + "] " +  "not FBA any more")
                #     self.__quit()
                #     return True

                else:
                    if self.amazon_item.status != AmazonItem.STATUS_ACTIVE:
                        self.__active_item()
                        self.status_updated = True
                        logger.info("[" + self.ebay_store.username + "][ASIN: " + self.amazon_item.asin + "] " +  "FBA and now active")

                    if offer_listing.best_fba_price != self.amazon_item.price: # price changed - update
                        self.__update_price(offer_listing.best_fba_price)
                        self.price_updated = True
                        logger.info("[" + self.ebay_store.username + "][ASIN: " + self.amazon_item.asin + "] " +  "FBA but price changed - found on other seller screen")
                    self.__update_review_count_and_avg_rating()
                self.__quit()
                return True
        else:
            # check enough stock available
            has_enough_stock = AmazonItemDetailPageSpider.has_enough_stock(self.driver)

            if not has_enough_stock:
                if self.amazon_item.status != AmazonItem.STATUS_OUT_OF_STOCK:
                    self.__oos_item()
                    self.status_updated = True
                    logger.info("[" + self.ebay_store.username + "][ASIN: " + self.amazon_item.asin + "] " +  "FBA but no enough stock")
                else:
                    logger.info("[" + self.ebay_store.username + "][ASIN: " + self.amazon_item.asin + "] " +  "FBA but still no enough stock")
                self.__quit()
                return True

            price_changed = self.__check_and_get_changed_price_on_item_screen()

            if price_changed == False:
                logger.info("[" + self.ebay_store.username + "][ASIN: " + self.amazon_item.asin + "] " +  "FBA and no price changed")
            else:
                self.__update_price(price_changed)
                self.price_updated = True
                logger.info("[" + self.ebay_store.username + "][ASIN: " + self.amazon_item.asin + "] " +  "FBA but price changed")

            self.__update_review_count_and_avg_rating()
            self.__quit()
            return True

        self.__quit()
        return True

    def __update_review_count_and_avg_rating(self):
        (review_count, avg_rating) = AmazonItemDetailPageSpider.get_reviewcount_and_avgrating(self.driver)
        try:
            if review_count:
                self.amazon_item.review_count = review_count
            if avg_rating:
                self.amazon_item.avg_rating = avg_rating
            amazon_item.updated_at = datetime.datetime.now()

            StormStore.add(amazon_item)
            StormStore.commit()
            return True
        
        except StormError, e:
            logger.exception("[" + self.ebay_store.username + "][ASIN: " + self.amazon_item.asin + "] " + "AmazonItem db review count / avg rating update error")
            StormStore.rollback()
        return False

    def __active_item(self):
        ebay_item_status = None if self.ebay_item == None else self.ebay_item.status
        return self.__update_status(AmazonItem.STATUS_ACTIVE, ebay_item_status)


    def __inactive_item(self):
        if self.ebay_item and self.ebay_item.status != EbayItem.STATUS_INACTIVE:
            ended = self.__end_ebay_item('NotAvailable')
            if ended:
                return self.__update_status(AmazonItem.STATUS_INACTIVE, EbayItem.STATUS_INACTIVE)

        return self.__update_status(AmazonItem.STATUS_INACTIVE)

    def __oos_item(self):
        """make ebay item to out of stock
        """
        if self.ebay_item:
            item_obj = generate_revise_inventory_status_obj(self.ebay_item, self.ebay_item.eb_price, 0)
            revised = self.__revise_ebay_item(item_obj)
            if revised:
                return self.__update_status(AmazonItem.STATUS_OUT_OF_STOCK, EbayItem.STATUS_OUT_OF_STOCK)

        return self.__update_status(AmazonItem.STATUS_OUT_OF_STOCK)

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
            token = None if settings.APP_ENV == 'stage' else self.ebay_store.token
            api = Trading(debug=True, warnings=True, domain=settings.EBAY_TRADING_API_DOMAIN, token=token, config_file=os.path.join(settings.CONFIG_PATH, 'ebay.yaml'))
            api.execute('EndItem', item_obj)

            if api.response.content:
                data = json.loads(api.response.json())

                # print json.dumps(data, indent=4, sort_keys=True)

                if ('ack' in data and data['ack'] == "Success") or ('Ack' in data and data['Ack'] == "Success"):
                    ret = True

                else:
                    logger.error(api.response.json())
                    record_trade_api_error(
                        item_obj['MessageID'], 
                        u'EndItem', 
                        utls.dict_to_json_string(item_obj),
                        api.response.json(),
                        amazon_item_id=self.amazon_item.id,
                        asin=self.amazon_item.asin,
                        ebay_item_id=self.ebay_item.id,
                        ebid=self.ebay_item.ebid
                    )

        except ConnectionError, e:
            logger.exception("[" + self.ebay_store.username + "][ASIN:" + self.amazon_item.asin + "] " + str(e))

        return ret

    def __update_status(self, am_status=None, eb_status=None):
        if am_status == None and eb_status == None:
            logger.error("[" + self.ebay_store.username + "] " + "No amazon status nor ebay status passed")
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
            logger.exception("[" + self.ebay_store.username + "][ASIN: " + self.amazon_item.asin + "] " + "AmazonItem / EbayItem db status update error")
            StormStore.rollback()
            return False

    def __update_price(self, amazon_price):
        if self.ebay_item:
            ebay_price = utils.calculate_profitable_price(amazon_price, self.ebay_store)
            
            item_obj = generate_revise_inventory_status_obj(self.ebay_item, ebay_price)

            revised = self.__revise_ebay_item(item_obj)

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

                    logger.info("[" + self.ebay_store.username + "][ASIN: " + self.amazon_item.asin + "] " + "PRICE UPDATED both amazon_item: $" + str(amazon_price) + ", and ebay_item: $" + str(ebay_price))

                except StormError, e:
                    logger.exception("[" + self.ebay_store.username + "][ASIN: " + self.amazon_item.asin + "] " + str(e))
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

                logger.info("[" + self.ebay_store.username + "][ASIN: " + self.amazon_item.asin + "] " + "PRICE UPDATED only at amazon_item: $" + str(amazon_price))

            except StormError, e:
                logger.exception("[" + self.ebay_store.username + "][ASIN: " + self.amazon_item.asin + "] " + str(e))

    def __revise_ebay_item(self, item_obj):

        ret = False

        try:
            token = None if settings.APP_ENV == 'stage' else self.ebay_store.token
            api = Trading(debug=True, warnings=True, domain=settings.EBAY_TRADING_API_DOMAIN, token=token, config_file=os.path.join(settings.CONFIG_PATH, 'ebay.yaml'))
            api.execute('ReviseInventoryStatus', item_obj)

            if api.response.content:
                data = json.loads(api.response.json())

                # print json.dumps(data, indent=4, sort_keys=True)

                if ('ack' in data and data['ack'] == "Success") or ('Ack' in data and data['Ack'] == "Success"):
                    ret = True

                elif ('ack' in data and data['ack'] == "Warning") or ('Ack' in data and data['Ack'] == "Warning"):

                    if data['Errors']['ErrorCode'] == "21919189" or data['Errors']['ErrorCode'] == 21919189:
                        ret = True
                        logger.warning("[ASIN: " + self.amazon_item.asin + "] " + data['Errors']['LongMessage'])
                    else:
                        logger.warning(api.response.json())
                        record_trade_api_error(
                            item_obj['MessageID'], 
                            u'ReviseInventoryStatus', 
                            utils.dict_to_json_string(item_obj),
                            api.response.json(), 
                            amazon_item_id=self.amazon_item.id,
                            asin=self.amazon_item.asin,
                            ebay_item_id=self.ebay_item.id,
                            ebid=self.ebay_item.ebid
                        )
                else:
                    # FixedPrice item ended. You are not allowed to revise an ended item
                    if data['Errors']['ErrorCode'] == "21916750" or data['Errors']['ErrorCode'] == 21916750:

                        # sync application's to ebay's status
                        self.__update_status(AmazonItem.STATUS_INACTIVE, EbayItem.STATUS_INACTIVE)
                        logger.warning("[EBID: " + self.ebay_item.ebid + "] " + data['Errors']['  LongMessage'])
                    else:
                        logger.error(api.response.json())
                        record_trade_api_error(
                            item_obj['MessageID'], 
                            u'ReviseInventoryStatus', 
                            utils.dict_to_json_string(item_obj),
                            api.response.json(), 
                            amazon_item_id=self.amazon_item.id,
                            asin=self.amazon_item.asin,
                            ebay_item_id=self.ebay_item.id,
                            ebid=self.ebay_item.ebid
                        )
        except ConnectionError, e:
            logger.exception("[ASIN:" + self.amazon_item.asin + "] " + str(e))

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


if __name__ == "__main__":

    task_option = 'all' if 'all' in sys.argv else ''

    if task_option == 'all':
        lock_file = os.path.join(settings.LOCK_PATH, 'amazon_item_monitor_all.lock')
    else:
        lock_file = os.path.join(settings.LOCK_PATH, 'amazon_item_monitor.lock')

    if os.path.isfile(lock_file):
        # this script is running by other process - exit
        die_message = 'amazon_item_monitor.py %s - This task is still running by other process. Ending this process.' % task_option
        logger.info(die_message)
        raise Exception(die_message)
    else:
        open(lock_file, 'w')
        logger.info('Lock file created - ' + lock_file)

    ebay_stores = StormStore.find(EbayStore, EbayStore.id != 3) # exclude wbjworld for now
    if ebay_stores.count() > 0:
        for ebay_store in ebay_stores:
            if task_option == 'all':
                # check all amazon items
                amazon_items = StormStore.find(AmazonItem,
                    LookupAmazonItem.amazon_item_id == AmazonItem.id,
                    LookupOwnership.lookup_id == LookupAmazonItem.lookup_id,
                    LookupOwnership.ebay_store_id == ebay_store.id,
                    AmazonItem.status != AmazonItem.STATUS_EXCLUDED) # chck whether excluded
            else:
                # check ebay listed items only
                amazon_items = StormStore.find(AmazonItem, 
                    AmazonItem.id == EbayItem.amazon_item_id,
                    EbayItem.ebay_store_id == ebay_store.id)

            num_status_updated = 0
            num_price_updated = 0

            if amazon_items.count() > 0:
                logger.info("[" + ebay_store.username + "] " + "Amazon items monitoring started...")
                
                for amazon_item in amazon_items:
                    monitor = AmazonItemMonitor(ebay_store, amazon_item)
                    monitor.run()

                    if monitor.status_updated:
                        logger.info("[" + ebay_store.username + "][ASIN: " + amazon_item.asin + "] " + "status changed to: " + str(amazon_item.status))
                        num_status_updated += 1

                    if monitor.price_updated:
                        logger.info("[" + ebay_store.username + "][ASIN: " + amazon_item.asin + "] " + "price changed to: " + str(amazon_item.price))
                        num_price_updated += 1

                logger.info("[" + ebay_store.username + "] " + "Number of amazon/ebay item status updated: " + str(num_status_updated) + " items")
                logger.info("[" + ebay_store.username + "] " + "Number of amazon/ebay item price updated: " + str(num_price_updated) + " items")

                # list items on ebay if necessary
                if num_status_updated > 0:
                    logger.info("[" + ebay_store.username + "] " + "start listing items on ebay")
                    handler = ListingHandler(ebay_store)
                    handler.run()

    if os.path.isfile(lock_file):
        os.remove(lock_file)
        logger.info('Lock file removed - ' + lock_file)

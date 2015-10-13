import sys, os
import datetime
import time

sys.path.append('%s/../../' % os.path.dirname(__file__))

import json

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException

from ebaysdk.trading import Connection as Trading
from ebaysdk.exception import ConnectionError

from amazonmws import settings
from amazonmws import utils
from amazonmws.models import StormStore, AmazonItem, AmazonItemPicture, Scraper, EbayItem, ItemQuantityHistory, Task
from amazonmws.errors import record_trade_api_error
from amazonmws.loggers import GrayLogger as logger, StaticFieldFilter, get_logger_name
from amazonmws.ebayapi.request_objects import generate_revise_inventory_status_obj

class EbayItemQuantityMonitor(object):

    ebay_item = None
    driver = None
    quantity_updated = False

    TASK_ID = Task.ebay_task_monitoring_quantity_changes

    min_quantity = 1

    def __init__(self, ebay_item):
        self.ebay_item = ebay_item
        self.driver = webdriver.PhantomJS()
        logger.addFilter(StaticFieldFilter(get_logger_name(), Task.get_name(self.TASK_ID)))

    def __del__(self):
        self.__quit()

    def __quit(self):
        if self.driver:
            self.driver.quit()

    def run(self):
        """ - check ebay quantity
        """

        logger.info("[EBID: " + self.ebay_item.ebid + "] " + "start mornitoring status")

        ebay_item_url = settings.EBAY_ITEM_LINK_FORMAT % self.ebay_item.ebid
        self.driver.get(ebay_item_url)

        # check ebay item quantity if it is low or not
        is_quantity_low = self.__is_qnt_low()

        if is_quantity_low:
            self.__update_item_quantity(settings.EBAY_ITEM_DEFAULT_QUANTITY)
            logger.info("[EBID: " + self.ebay_item.ebid + "] " +  "quantity was low. now updated successfully")
            self.__quit()
            self.quantity_updated = True
            return True

        self.__quit()
        return True

    def __is_qnt_low(self):
        is_quantity_low = False

        try:
            wait = WebDriverWait(self.driver, settings.APP_DEFAULT_WEBDRIVERWAIT_SEC)
            quantity_container = wait.until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="v4-26"]/*/span[contains(@class, "vi-is1-mqtyDiv")]' if settings.APP_ENV == 'stage' else '//*[@id="qtySubTxt"]'))
            )
            element_text = quantity_container.text
            ints = [int(s) for s in element_text.split() if s.isdigit()]
            quantity = ints[0]

            if quantity < self.min_quantity:
                is_quantity_low = True

        except NoSuchElementException, e:
            logger.exception(e)
        
        except StaleElementReferenceException, e:
            logger.exception(e)

        except TimeoutException:
            utils.take_screenshot(self.driver, 'no-qnt-' + self.ebay_item.ebid + '-' + str(time.time()) + '.png')            
            logger.exception("[url: " + self.driver.current_url + "] " + "CSS Selector Error: unable to find quantity element")

        return is_quantity_low

    def __update_item_quantity(self, quantity):
        added = self.__add_more_ebay_item_quantity(quantity)
        if added:
            self.__record_history(quantity)

    def __add_more_ebay_item_quantity(self, quantity):
        ret = False

        item_obj = generate_revise_inventory_status_obj(self.ebay_item, None, quantity)

        try:
            api = Trading(debug=True, warnings=True, domain=settings.EBAY_TRADING_API_DOMAIN)
            api.execute('ReviseInventoryStatus', item_obj)

            if api.response.content:
                data = json.loads(api.response.json())

                # print json.dumps(data, indent=4, sort_keys=True)

                if ('ack' in data and data['ack'] == "Success") or ('Ack' in data and data['Ack'] == "Success"):
                    ret = True

                else:
                    logger.error(api.response.json())
                    record_trade_api_error(
                        item_obj['MessageID'], 
                        u'ReviseInventoryStatus', 
                        utils.dict_to_json_string(item_obj),
                        api.response.json(), 
                        amazon_item_id=self.ebay_item.amazon_item_id,
                        asin=self.ebay_item.asin,
                        ebay_item_id=self.ebay_item.id,
                        ebid=self.ebay_item.ebid
                    )

        except ConnectionError, e:
            logger.exception("[ASIN:" + self.amazon_item.asin + "] " + str(e))

        return ret

    def __record_history(self, quantity):
        try:
            quantity_history = ItemQuantityHistory()
            quantity_history.amazon_item_id = self.ebay_item.amazon_item_id
            quantity_history.asin = self.ebay_item.asin
            quantity_history.ebay_item_id = self.ebay_item.id
            quantity_history.ebid = self.ebay_item.ebid
            quantity_history.quantity = quantity
            quantity_history.created_at = datetime.datetime.now()
            quantity_history.updated_at = datetime.datetime.now()
            StormStore.add(quantity_history)
            StormStore.commit()
            return True

        except StormError, e:
            logger.exception("[EBID: " + self.ebay_item.ebid + "] " + "ItemQuantityHistory insert error")
            StormStore.rollback()
            return False


if __name__ == "__main__":
    
    active_ebay_items = StormStore.find(EbayItem, EbayItem.status == EbayItem.STATUS_ACTIVE)
    num_updated = 0

    if active_ebay_items.count() > 0:
        for ebay_item in active_ebay_items:
            monitor = EbayItemQuantityMonitor(ebay_item)
            monitor.run()

            if monitor.quantity_updated:
                logger.info("[EBID: " + ebay_item.ebid + "] " + "quantity updated to " + settings.EBAY_ITEM_DEFAULT_QUANTITY)
                num_updated += 1
        
        logger.info("Number of ebay item quantity updated: " + str(num_updated) + " items")


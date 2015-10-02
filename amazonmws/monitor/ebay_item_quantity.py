import sys, os

sys.path.append('%s/../../' % os.path.dirname(__file__))

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException

from amazonmws import settings
from amazonmws.models import StormStore, AmazonItem, AmazonItemPicture, Scraper, ScraperAmazonItem, EbayItem, EbayListingError, ItemQuantityHistory, Task
from amazonmws.loggers import GrayLogger as logger, StaticFieldFilter, get_logger_name
from amazonmws.monitor.amazon_item import PriceMonitor
from amazonmws.ebaystore.listing import OnError



class EbayItemQuantityMonitor(object):

    ebay_item = None
    driver = None
    page_opened = True
    quantity_updated = False

    TASK_ID = Task.ebay_task_monitoring_quantity_changes

    min_quantity = 5

    def __init__(self, ebay_item):
        self.ebay_item = ebay_item
        self.driver = webdriver.PhantomJS()
        logger.addFilter(StaticFieldFilter(get_logger_name(), Task.get_name(self.TASK_ID)))

    def __del__(self):
        self.__quit()

    def __quit(self):
        if self.driver:
            self.driver.quit()

        self.page_opened = False

    def run(self):
        """ - check ebay quantity
        """

        logger.info("[EBID: " + self.ebay_item.ebid + "] " + "start mornitoring status")

        ebay_item_url = settings.EBAY_ITEM_LINK_PREFIX + self.ebay_item.ebid
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

    @staticmethod
    def quantity_low_indicator(driver):

        css_selector = '.vi-is1-mqtyDiv' if settings.APP_ENV == 'stage' else '#qtySubTxt'

        # print css_selector

        element_text = driver.find_element_by_css_selector(css_selector).text
        string_quantity = element_text.strip('available').strip()

        # print string_quantity

        quantity = int(string_quantity)

        # print quantity

        if quantity < EbayItemQuantityMonitor.min_quantity:
            return True

        return False

    def __is_qnt_low(self):

        is_quantity_low = False

        try:
            wait = WebDriverWait(self.driver, 10)
            is_quantity_low = wait.until(EbayItemQuantityMonitor.quantity_low_indicator)

        except NoSuchElementException, e:
            logger.exception(e)
        
        except StaleElementReferenceException, e:
            logger.exception(e)

        except TimeoutException:
            logger.exception("[url: " + self.driver.current_url + "] " + "CSS Selector Error: unable to find quantity element")

        return is_quantity_low

    def __update_item_quantity(self, quantity):
        added = self.__add_more_ebay_item_quantity(quantity)
        if added:
            self.__record_history(quantity)

    def __add_more_ebay_item_quantity(self, quantity):
        ret = False

        item_obj = PriceMonitor.generate_ebay_revise_inventory_status_obj(self.ebay_item, None, quantity)

        try:
            api = Trading(debug=True, warnings=True, domain=settings.EBAY_TRADING_API_DOMAIN)
            api.execute('ReviseInventoryStatus', item_obj)

            if api.response.content:
                data = json.loads(api.response.json())

                # print json.dumps(data, indent=4, sort_keys=True)

                if ('ack' in data and data['ack'] == "Success") or ('Ack' in data and data['Ack'] == "Success"):
                    ret = True

                else:
                    self.__log_on_error(unicode(api.response.json()), u'ReviseInventoryStatus')

        except ConnectionError, e:
            self.__log_on_error(e, unicode(e.response.dict()), u'ReviseInventoryStatus')

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

    def __log_on_error(self, e, reason, related_ebay_api=u''):
        OnError(e, None,
            EbayListingError.TYPE_ERROR_ON_REVISE_QUANTITY,
            reason,
            related_ebay_api,
            self.ebay_item)


if __name__ == "__main__":
    
    active_ebay_items = StormStore.find(EbayItem, EbayItem.status == EbayItem.STATUS_ACTIVE)
    num_updated = 0

    if active_ebay_items.count() > 0:
        for ebay_item in active_ebay_items:
            monitor = EbayItemQuantityMonitor(ebay_item)
            monitor.run()

            while monitor.page_opened:
                if not monitor.page_opened:
                    if monitor.quantity_updated:
                        logger.info("[EBID: " + ebay_item.ebid + "] " + "quantity updated to 20: " + str(self.amazon_item.status))
                        num_updated += 1

                    break
        
        logger.info("Number of ebay item quantity updated: " + str(num_updated) + " items")


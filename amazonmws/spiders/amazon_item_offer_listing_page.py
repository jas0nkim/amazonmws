import sys, traceback
import datetime, time
import re
from decimal import Decimal

# from pyvirtualdisplay import Display

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException

from storm.exceptions import StormError

from amazonmws import settings
from amazonmws import utils
from amazonmws.models import StormStore, AmazonItem, AmazonItemPicture, ScraperAmazonItem, Scraper, Task
from amazonmws.loggers import GrayLogger as logger, StaticFieldFilter, get_logger_name


class AmazonItemOfferListingPageSpiderException(Exception):
    pass

class AmazonItemOfferListingPageSpider(object):

    __driver = None
    __url = None
    __task_id = 0

    asin = None
    is_fba = False
    best_fba_price = None

    def __init__(self, asin, task_id=1):
        # install phantomjs binary file - http://phantomjs.org/download.html
        self.__driver = webdriver.PhantomJS()
        self.__url = settings.AMAZON_ITEM_OFFER_LISTING_LINK_FORMAT % asin
        self.__task_id = task_id

        self.asin = asin
        logger.addFilter(StaticFieldFilter(get_logger_name(), Task.get_name(self.__task_id)))

    def __del__(self):
        self.__quit()

    def __quit(self):
        if self.__driver:
            self.__driver.quit()

    def load(self):
        self.__driver.get(self.__url)

        try:
            # now screen moved to other sellers for this item
            wait = WebDriverWait(self.__driver, settings.APP_DEFAULT_WEBDRIVERWAIT_SEC)
            olp_container = wait.until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="olpTabContent"]/div/div[@role="main"]/div[contains(@class, "olpOffer")]/div[1]/span[contains(@class, "supersaver")]/i[contains(@class, "a-icon-prime")]'))
            )
        except TimeoutException, e:
            utils.take_screenshot(self.__driver, 'no-olp-' + self.asin + '-' + str(time.time()) + '.png')
            logger.exception("[" + self.__url + "] " + str(e))
            self.__quit()
            raise AmazonItemOfferListingPageSpiderException("[ASIN: " + self.asin + "] " + "Unable to find FBA offers from the list")
            
        prime_icon_on_best_offer = self.__driver.find_element_by_xpath('(//*[@id="olpTabContent"]/div/div[@role="main"]/div[contains(@class, "olpOffer")]/div[1]/span[contains(@class, "supersaver")]/i[contains(@class, "a-icon-prime")])[1]')

        try:
            self.best_fba_price = Decimal(prime_icon_on_best_offer.find_element_by_xpath("../../span[1]").text.strip('$').strip()).quantize(Decimal('1.00'))

            self.is_fba = True

        except NoSuchElementException, e:
            logger.exception("[ASIN: " + self.asin + "] " + "No fba price available")
            self.__quit()
            raise AmazonItemOfferListingPageSpiderException("[ASIN: " + self.asin + "] " + "FBA offer found, but failed to retrieve the price")
        
        except StaleElementReferenceException, e:
            logger.exception(e)
            self.__quit()
            raise AmazonItemOfferListingPageSpiderException()

        self.__quit()
        return True



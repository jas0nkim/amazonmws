import sys, traceback
import re
from urllib2 import URLError

from scrapy.spiders import CrawlSpider
from scrapy import Selector
from scrapy.http import Request

# from pyvirtualdisplay import Display

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException

from amazonmws import settings
from amazonmws.models import StormStore, AmazonItem, Scraper, LookupAmazonItem
from amazonmws.loggers import GrayLogger as logger, StaticFieldFilter, get_logger_name

from .amazon_item_detail_having_variations_page import AmazonItemDetailHavingVariationsPageSpider


class KeywordsSpider(CrawlSpider):
    """KeywordsSpider

    A spider to discover items by keywords from amazon.com site

    """
    name = "keywords"
    allowed_domains = ["www.amazon.com"]

    start_urls = []

    SCRAPER_ID = 0

    def __init__(self):
        CrawlSpider.__init__(self)
        self.verificationErrors = []
        # install phantomjs binary file - http://phantomjs.org/download.html
        self.driver = webdriver.PhantomJS()
        logger.addFilter(StaticFieldFilter(get_logger_name(), Scraper.get_name(self.SCRAPER_ID)))

        # use firefox & vertual display instead. phantomjs cannot capture elements some cases.
        # ref: http://stackoverflow.com/a/23447450
        # if 'linux' in sys.platform:
        #     self.display = Display(visible=0, size=(1280, 800))
        #     self.display.start()
        # self.driver = webdriver.Firefox()

    def __del__(self):
        self.__quit()
        logger.error(', '.join(self.verificationErrors))
        CrawlSpider.__del__(self)

    def __quit(self):
        if self.driver:
            self.driver.quit()
        # if 'linux' in sys.platform and self.display:
        #     self.display.stop()

    def parse(self, response):
        if self.lookups != None:
            for lookup in self.lookups:
                self.parse_category(lookup.url, lookup.id)
        else:
            url = response.url
            self.parse_category(url)

        self.__quit()

    def parse_category(self, url, current_lookup_id=None):
        """recursion
        """
        self.driver.get(url)

        try:
            wait_category = WebDriverWait(self.driver, settings.APP_DEFAULT_WEBDRIVERWAIT_SEC)
            categories = wait_category.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#refinements .categoryRefinementsSection ul li:not(.shoppingEngineExpand)'))
            )
            current_category = wait_category.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#refinements .categoryRefinementsSection ul li:not(.shoppingEngineExpand) strong'))
            )
        except TimeoutException, e:
            logger.exception(e)
            return

        sub_categories = categories

        logger.info('num of sub categories (categories): ' + str(len(sub_categories)))

        if len(sub_categories) < 2:
            logger.info("[" + Scraper.get_name(self.SCRAPER_ID) + "][url:" + url + "] " + "CATEGORY: " + current_category.text + " - leaf category")
            self.parse_page(current_category.text, current_lookup_id)

        else:
            logger.info("[" + Scraper.get_name(self.SCRAPER_ID) + "][url:" + url + "] " + "CATEGORY: " + current_category.text)
            sub_category_links = []

            # had to go with this direction - collect (loop) urls first and loop throw the urls one more time
            # due to StaleElementReferenceException raises
            for sub_category in sub_categories:
                try:
                    sub_category_links.append(sub_category.find_element_by_css_selector('a').get_attribute('href'))

                except NoSuchElementException, e:
                    logger.warning('no anchor found')
                
                except StaleElementReferenceException, e:
                    logger.exception(e)

            for sub_category_link in sub_category_links:
                try:
                    self.parse_category(sub_category_link, current_lookup_id)

                except URLError, e:
                    logger.exception(e)
    
    def parse_page(self, category_name, current_lookup_id=None):
        current_page_num = 0

        while True:

            current_page_num += 1

            logger.info("[" + Scraper.get_name(self.SCRAPER_ID) + "] " + category_name + " [PAGE " + str(current_page_num) + "]")

            # find all items from the page
            # list of WebElement
            # https://selenium-python.readthedocs.org/api.html?highlight=click#selenium.webdriver.remote.webelement.WebElement
            items = self.driver.find_elements_by_css_selector('ul#s-results-list-atf li.s-result-item')
            
            current_item_num = 0

            while len(items) >= current_item_num:

                current_item_num += 1
                match = False

                # hyperlink
                try:
                    hyperlink = self.driver.find_element_by_css_selector('ul#s-results-list-atf li.s-result-item:nth-child('+str(current_item_num)+') a.s-access-detail-page').get_attribute('href')
                    match = re.match(settings.AMAZON_ITEM_LINK_PATTERN, hyperlink)

                except NoSuchElementException:
                    logger.exception('No title hyperlink element')
                
                except StaleElementReferenceException, e:
                    logger.exception(e)

                if match:
                    existing_amazon_item = StormStore.find(AmazonItem, AmazonItem.asin == match.group(3)).one()

                    if existing_amazon_item:
                        existing_lookup = StormStore.find(LookupAmazonItem, LookupAmazonItem.amazon_item_id == existing_amazon_item.id).one()
                        if not existing_lookup:
                            self.__add_lookup_relationship(existing_amazon_item, current_lookup_id)
                        else:
                            logger.info("[ASIN:" + existing_amazon_item.asin + "] " + " already exists in database")
                            continue
                    else:
                        detail_page_spider = AmazonItemDetailHavingVariationsPageSpider(match.group(0), self.SCRAPER_ID, current_lookup_id)
                        detail_page_spider.load()
                else:
                    logger.warning("[url:" + hyperlink + "] " + "failed to retrieve asin from the url")
                    continue

            try:
                # move to next page in pagenation
                next_page_num = current_page_num + 1
                next_page_link = self.driver.find_element_by_css_selector('#pagn a#pagnNextLink')
                next_page_link.click()

                wait = WebDriverWait(self.driver, settings.APP_DEFAULT_WEBDRIVERWAIT_SEC)
                wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "li.s-result-item"))
                )

            except NoSuchElementException:
                logger.exception('No more next page')
                break
            
            except StaleElementReferenceException, e:
                logger.exception(e)
                break

            except TimeoutException, e:
                logger.exception(e)
                break


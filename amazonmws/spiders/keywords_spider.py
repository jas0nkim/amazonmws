import sys, traceback
from os.path import basename
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
from amazonmws.models import StormStore, AmazonItem, ScraperAmazonItem, Scraper
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
        url = response.url
        self.parse_category(url)
        self.__quit()

    def parse_category(self, url):
        """recursion
        """
        self.driver.get(url)

        selected_categories = []

        try:
            wait_category = WebDriverWait(self.driver, 10)
            wait_category.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#refinements .categoryRefinementsSection ul.root li"))
            )
            
        except TimeoutException:
            logger.exception('Timeout exception raised')

        category_tree = self.driver.find_element_by_css_selector('#refinements .categoryRefinementsSection')

        selected_categories = category_tree.find_elements_by_xpath('.//strong') # get last element from this list

        if len(selected_categories) < 1:
            return

        current_category = selected_categories[-1]

        logger.info("[" + basename(__file__) + "] " + "CATEGORY " + current_category.text)

        li = current_category.find_element_by_xpath('../..')

        has_sub = False

        try:
            has_sub = li.find_element_by_xpath('.//ul')

        except NoSuchElementException:
            logger.exception('No more subcategory')
        
        except StaleElementReferenceException, e:
            logger.exception(e)

        if has_sub is False:
            self.parse_page(current_category.text)
            return

        else:
            sub_category_lists = has_sub.find_elements_by_xpath('.//li')
            sub_category_links = []

            # had to go with this direction - collect (loop) urls first and loop throw the urls one more time
            # due to StaleElementReferenceException raises
            for sub_category in sub_category_lists:

                sub_category_links.append(sub_category.find_element_by_xpath('.//a').get_attribute('href'))

            for sub_category_link in sub_category_links:
                try:
                    self.parse_category(sub_category_link)

                except NoSuchElementException:
                    logger.exception('No more subcategory link')
                
                except StaleElementReferenceException, e:
                    logger.exception(e)

                except URLError, e:
                    logger.exception(e)
    
    def parse_page(self, category_name):
        current_page_num = 0

        while True:

            current_page_num += 1

            logger.info("[" + basename(__file__) + "] " + category_name + " [PAGE " + str(current_page_num) + "]")

            # find all best seller items from the page
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
                    # check if the item already exists in database
                    asin_already_exists = StormStore.find(AmazonItem, AmazonItem.asin == match.group(3)).one()

                    asin_already_scraped_by_this =  StormStore.find(ScraperAmazonItem, ScraperAmazonItem.scraper_id == self.SCRAPER_ID, ScraperAmazonItem.asin == match.group(3)).one()

                    if not asin_already_scraped_by_this and not asin_already_exists:
                        
                        detail_page_spider = AmazonItemDetailHavingVariationsPageSpider(match.group(0), self.SCRAPER_ID)
                        detail_page_spider.load()

                        while True:
                            if detail_page_spider.page_opened == False:
                                break
                    else:
                        logger.info("[" + basename(__file__) + "] " + match.group(3) + ' already exists in database')

            try:
                # move to next page in pagenation
                next_page_num = current_page_num + 1
                next_page_link = self.driver.find_element_by_css_selector('#pagn a#pagnNextLink')
                next_page_link.click()

                wait = WebDriverWait(self.driver, 10)
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


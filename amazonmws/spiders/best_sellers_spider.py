import sys, traceback
import re
from urllib2 import URLError

from scrapy.spiders import CrawlSpider
from scrapy import Selector
from scrapy.http import Request

from pyvirtualdisplay import Display

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException

from amazonmws import settings
from amazonmws.models import StormStore, AmazonItem, ScraperAmazonItem
from amazonmws.spiders.amazon_item_detail_page import AmazonItemDetailPageSpider

class BestSellersSpider(CrawlSpider):
    """BestSellersSpider

    A spider to discover best seller items from amazon.com site - sub-directories of http://www.amazon.com/Best-Sellers/zgbs

    """
    name = "bestsellers"
    allowed_domains = ["www.amazon.com"]
    start_urls = []

    # SCRAPER_ID = 0

    def __init__(self):
        CrawlSpider.__init__(self)
        self.verificationErrors = []
        # install phantomjs binary file - http://phantomjs.org/download.html
        # self.driver = webdriver.PhantomJS()

        # use firefox & vertual display instead. phantomjs cannot capture elements some cases.
        # ref: http://stackoverflow.com/a/23447450
        if 'linux' in sys.platform:
            self.display = Display(visible=0, size=(1280, 800))
            self.display.start()
        self.driver = webdriver.Firefox()

    def __del__(self):
        self.__quit()
        print self.verificationErrors
        CrawlSpider.__del__(self)

    def __quit(self):
        if self.driver:
            self.driver.quit()
        if 'linux' in sys.platform and self.display:
            self.display.stop()

    def parse(self, response):
        url = response.url
        self.parse_category(url)
        self.__quit()

    def parse_category(self, url):
        """recursion
        """
        self.driver.get(url)
        
        category_tree = self.driver.find_element_by_css_selector('#zg_browseRoot')
        current_category = category_tree.find_element_by_css_selector('li span.zg_selected')

        print "="*10
        print "="*10 + " CATEGORY " + current_category.text + " " + "="*10
        print "="*10

        ul = current_category.find_element_by_xpath('../..')

        has_sub = False

        try:
            has_sub = ul.find_element_by_xpath('.//ul')

        except NoSuchElementException as err:
            print 'No more subcategory:', err
        
        except StaleElementReferenceException as err:
            print 'Element is no longer attached to the DOM:', err

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

                except NoSuchElementException as err:
                    print 'No subcategory link', err
                    print '-'*60
                    traceback.print_exc(file=sys.stdout)
                    print '-'*60
                
                except StaleElementReferenceException as err:
                    print 'Element is no longer attached to the DOM', err
                    print '-'*60
                    traceback.print_exc(file=sys.stdout)
                    print '-'*60

                except URLError as err:
                    print "url error - " + sub_category_link + ":", err
                    print '-'*60
                    traceback.print_exc(file=sys.stdout)
                    print '-'*60
    
    def parse_page(self, category_name):
        page_container = self.driver.find_element_by_css_selector('ol.zg_pagination')
        current_page_num = 0

        while True:

            current_page_num += 1

            print "*"*10
            print "*"*10 + " " + category_name + " [PAGE " + str(current_page_num) + "] " + "*"*10
            print "*"*10

            # find all best seller items from the page
            # list of WebElement
            # https://selenium-python.readthedocs.org/api.html?highlight=click#selenium.webdriver.remote.webelement.WebElement
            items = self.driver.find_elements_by_css_selector('#zg_centerListWrapper .zg_itemWrapper')
            
            for item in items:

                match = False

                # hyperlink
                try:
                    hyperlink = item.find_element_by_css_selector('.zg_title a').get_attribute('href')
                    match = re.match(settings.AMAZON_ITEM_LINK_PATTERN, hyperlink)

                except NoSuchElementException as err:
                    print 'No title hyperlink element:', err
                
                except StaleElementReferenceException as err:
                    print 'Element is no longer attached to the DOM:', err

                if match:
                    # check if the item already exists in database
                    asin_already_exists = StormStore.find(AmazonItem, AmazonItem.asin == match.group(3)).one()

                    asin_already_scraped_by_this =  StormStore.find(ScraperAmazonItem, ScraperAmazonItem.scraper_id == self.SCRAPER_ID, ScraperAmazonItem.asin == match.group(3)).one()

                    if not asin_already_scraped_by_this and not asin_already_exists:
                        
                        detail_page_spider = AmazonItemDetailPageSpider(match.group(0), self.SCRAPER_ID)
                        detail_page_spider.load()

                        while True:
                            if detail_page_spider.page_opened == False:
                                break
                    else:
                        print match.group(3) + ' already exists in database'

            try:
                # move to next page in pagenation
                next_page_num = current_page_num + 1
                next_page_link = page_container.find_element_by_css_selector('li.zg_page:nth-child(' + str(next_page_num) + ') a')
                next_page_link.click()

                wait = WebDriverWait(self.driver, 10)
                wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".zg_itemWrapper"))
                )

            except NoSuchElementException as err:
                print 'No more next page:', err
                break
            
            except StaleElementReferenceException as err:
                print 'Element is no longer attached to the DOM:', err
                break

            except TimeoutException as err:
                print 'Timeout exception raised:', err
                break


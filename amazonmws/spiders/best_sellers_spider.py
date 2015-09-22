import re
from urllib2 import URLError

from scrapy.spiders import CrawlSpider
from scrapy import Selector
from scrapy.http import Request

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException

from amazonmws import settings
from amazonmws.models import StormStore, AmazonItem
from amazonmws.spiders.amazon_item_detail_page import AmazonItemDetailPageSpider

class BestSellersSpider(CrawlSpider):
    """BestSellersSpider

    A spider to discover best seller items from amazon.com site - sub-directories of http://www.amazon.com/Best-Sellers/zgbs

    """
    name = "bestsellers"
    allowed_domains = ["www.amazon.com"]
    start_urls = [
        # Best Sellers - Toys and Games
        "http://www.amazon.com/Best-Sellers-Toys-Games/zgbs/toys-and-games",
    ]

    def __init__(self):
        CrawlSpider.__init__(self)
        self.verificationErrors = []
        # install phantomjs binary file - http://phantomjs.org/download.html
        self.driver = webdriver.PhantomJS()

    def __del__(self):
        self.__quit()
        print self.verificationErrors
        CrawlSpider.__del__(self)

    def __quit(self):
        if self.driver:
            self.driver.quit()

    def parse(self, response):
        url = response.url
        self.parse_category(url)

    def parse_category(self, url):
        """recursion
        """
        self.driver.get(url)
        current_category = self.driver.find_element_by_css_selector('li span.zg_selected')

        print "=========="
        print "========== CATEGORY " + current_category.text + " =========="
        print "=========="

        ul = current_category.find_element_by_xpath('../..')

        has_sub = False

        try:
            has_sub = ul.find_element_by_xpath('.//ul')

        except NoSuchElementException:
            print 'No more subcategory'
        
        except StaleElementReferenceException:
            print 'Element is no longer attached to the DOM'

        if has_sub is False:
            self.parse_page(current_category.text)

        else:
            sub_category_lists = has_sub.find_elements_by_xpath('.//li')
            for sub_category in sub_category_lists:
                try:
                    sub_category_link = sub_category.find_element_by_xpath('.//a').get_attribute('href')
                    self.parse_category(sub_category_link)

                except NoSuchElementException:
                    print 'No subcategory link'
                
                except StaleElementReferenceException:
                    print 'Element is no longer attached to the DOM'

                except URLError:
                    print "url error: " + sub_category_link
    
    def parse_page(self, category_name):
        page_container = self.driver.find_element_by_css_selector('ol.zg_pagination')
        current_page_num = 0

        while True:

            current_page_num += 1

            print "**********"
            print "********** " + category_name + " [PAGE " + str(current_page_num) + "] **********"
            print "**********"

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

                except NoSuchElementException:
                    print 'No title hyperlink element'
                
                except StaleElementReferenceException:
                    print 'Element is no longer attached to the DOM'

                if match:
                    # check if the item already exists in database
                    already_exists = StormStore.find(AmazonItem, AmazonItem.asin == match.group(3)).one()

                    if not already_exists:
                        while True:
                            detail_page_spider = AmazonItemDetailPageSpider(match.group(0))
                            detail_page_spider.load()

                            if detail_page_spider.page_opened == False:
                                break
                    else:
                        print match.group(3) + ' already exists in database'

            try:
                next_page_num = current_page_num + 1
                next_page_link = page_container.find_element_by_css_selector('li.zg_page:nth-child(' + str(next_page_num) + ') a')
                next_page_link.click()

                wait = WebDriverWait(self.driver, 10)
                wait.until(
                    EC.invisibility_of_element_located((By.CSS_SELECTOR, ".zg_itemWrapper"))
                )

            except NoSuchElementException:
                print 'No more next page'
                break
            
            except StaleElementReferenceException:
                print 'Element is no longer attached to the DOM'
                break

            except TimeoutException:
                print 'Timeout exception raised'
                break

        self.__quit()

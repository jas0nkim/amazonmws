import re

from scrapy.spiders import CrawlSpider
from scrapy import Selector
from scrapy.http import Request

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

from amazonmws import settings
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
        self.driver.get(response.url)

        while True:
            
            # find all best seller items from the page
            # list of WebElement
            # https://selenium-python.readthedocs.org/api.html?highlight=click#selenium.webdriver.remote.webelement.WebElement
            items = self.driver.find_elements_by_css_selector('#zg_centerListWrapper .zg_itemWrapper')
            
            count_prime_items = 0
            
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

                    while True:

                        detail_page_spider = AmazonItemDetailPageSpider(match.group(0))
                        detail_page_spider.load()

                        count_prime_items += 1

                        if detail_page_spider.page_opened == False:
                            break

            # print item count
            print 'total prime items: ' + str(count_prime_items)
            break

            # try:
            #     next.click()

            #     # get the data and write it to scrapy items
            # except:
            #     break

        self.__quit()

import time
import datetime
import re

from scrapy.spiders import CrawlSpider
from scrapy import Selector
from scrapy.http import Request

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

from storm.locals import *

from amazonmws import settings
from amazonmws.models import StormStore

class DiscoverySpider(CrawlSpider):
    """DiscoverySpider

    A spider to discover new items from amazon.com site. Start urls are used by keywords.

    """    
    name = "discovery"
    allowed_domains = ["www.amazon.com"]
    start_urls = [
        # laptop
        "http://www.amazon.com/s/ref=nb_sb_ss_c_0_6?url=search-alias%3Dcomputers&field-keywords=laptop",
        # tablet
        "http://www.amazon.com/s/ref=nb_sb_ss_c_0_6?url=search-alias%3Dcomputers&field-keywords=tablet",
    ]

    def __init__(self):
        CrawlSpider.__init__(self)
        self.verificationErrors = []
        # install phantomjs binary file - http://phantomjs.org/download.html
        self.driver = webdriver.PhantomJS()

        # use firefox instead. phantomjs cannot capture elements some cases.
        # self.driver = webdriver.Firefox()

    def __del__(self):
        self.driver.quit()
        print self.verificationErrors
        CrawlSpider.__del__(self)

    def parse(self, response):
        self.parse_list_page(response)


    def parse_list_page(self, response):
        self.driver.get(response.url)

        while True:
            # find all items from the page
            items = self.driver.find_elements_by_css_selector('li.s-result-item')
            count_prime_items = 0
            for item in items:
                # filter prime items
                prime_item = False
                try:
                    prime_logo = item.find_element_by_css_selector('i.a-icon-prime')
                    if prime_logo:
                        prime_item = True
                
                except NoSuchElementException:
                    print 'No i.a-icon-prime element'
                
                except StaleElementReferenceException:
                    print 'Element is no longer attached to the DOM'

                if prime_item:

                    detail_link_element = None

                    try:
                        detail_link_element = item.find_element_by_css_selector('a.s-access-detail-page')
                        title = detail_link_element.text
                        hyperlink = detail_link_element.get_attribute('href')
                        match = re.match(settings.AMAZON_ITEM_LINK_PATTERN, hyperlink)
                        if match:

                            # discovered_item = DiscoveredItem()
                            # discovered_item.url = match.group(0)
                            # discovered_item.asin = match.group(3)
                            # discovered_item.title = title
                            # discovered_item.created_at = datetime.datetime.now()
                            # discovered_item.updated_at = datetime.datetime.now()

                            # StormStore.add(discovered_item)
                            # StormStore.commit()

                            count_prime_items += 1
                        else:
                            print hyperlink + ' not matched'
                    
                    except NoSuchElementException:
                        print 'No a.s-access-detail-page element'
                    
                    except StaleElementReferenceException:
                        print 'Element is no longer attached to the DOM'




            # print items

            print 'total prime items: ' + str(count_prime_items)
            break

            try:
                next.click()

                # get the data and write it to scrapy items
            except:
                break

    def parse_item_detail_page(self, response):
        pass

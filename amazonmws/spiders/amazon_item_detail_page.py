import datetime
import re
from decimal import Decimal

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException

from amazonmws import settings
from amazonmws.models import StormStore, AmazonItem

class AmazonItemDetailPageSpider(object):

    page_opened = False
    url = None

    def __init__(self, url):
        # install phantomjs binary file - http://phantomjs.org/download.html
        self.driver = webdriver.PhantomJS()
        self.page_opened = True
        self.url = url

    def __del__(self):
        self.__quit()

    def __quit(self):
        if self.driver:
            self.driver.quit()
        self.page_opened = False

    def load(self):
        self.driver.get(self.url)

        is_fba = False

        try:
            wait = WebDriverWait(self.driver, 10)
            is_fba = wait.until(
                EC.invisibility_of_element_located((By.CSS_SELECTOR, "#bbop-check-box"))
            )

        except NoSuchElementException:
            print 'No prime element'
        
        except StaleElementReferenceException:
            print 'Element is no longer attached to the DOM'

        except TimeoutException:
            print 'Timeout exception raised'

        if is_fba != False:
            self.__parse()

        else:
            print self.url + " NO FBA"

        self.__quit()

    def __parse(self):
        category = None
        subcategory = None
        description = None

        try:

            breadcrumbs = self.driver.find_element_by_css_selector('#wayfinding-breadcrumbs_container ul')

            # category
            try:
                category = breadcrumbs.find_element_by_css_selector('li:not(.a-breadcrumb-divider):first-child span.a-list-item').text
            except NoSuchElementException:
                print 'No breadcrumb category element'
            
            except StaleElementReferenceException:
                print 'Element is no longer attached to the DOM'

            # sub-category
            try:
                subcategory = breadcrumbs.find_element_by_css_selector('li:not(.a-breadcrumb-divider):nth-child(2) span.a-list-item').text
            except NoSuchElementException:
                print 'No breadcrumb sub-category element'
            
            except StaleElementReferenceException:
                print 'Element is no longer attached to the DOM'

            # description
            try:
                description = self.driver.find_element_by_css_selector('#productDescription').get_attribute('innerHTML')
            except NoSuchElementException:
                print 'No description element'
            
            except StaleElementReferenceException:
                print 'Element is no longer attached to the DOM'

            summary_section = self.driver.find_element_by_css_selector('#centerCol')
            title = summary_section.find_element_by_css_selector('h1#title').text

            # price
            price = Decimal(summary_section.find_element_by_css_selector('#priceblock_ourprice').text.strip()[1:]).quantize(Decimal('1.00'))

            hyperlink = self.url
            match = re.match(settings.AMAZON_ITEM_LINK_PATTERN, hyperlink)

            if match:
                amazon_item = AmazonItem()
                amazon_item.url = match.group(0)
                amazon_item.asin = match.group(3)
                if category:
                    amazon_item.category = category
                if subcategory:
                    amazon_item.subcategory = subcategory
                amazon_item.title = title
                amazon_item.price = price
                if description:
                    amazon_item.description = description
                amazon_item.status = 1
                amazon_item.created_at = datetime.datetime.now()
                amazon_item.updated_at = datetime.datetime.now()

                StormStore.add(amazon_item)
                StormStore.commit()

            else:
                print hyperlink + ' not matched'
        
        except NoSuchElementException:
            print 'No element'
        
        except StaleElementReferenceException:
            print 'Element is no longer attached to the DOM'

import datetime
import re
from decimal import Decimal

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException

from storm.exceptions import StormError

from amazonmws import settings
from amazonmws.models import StormStore, AmazonItem, AmazonItemPicture

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

        except NoSuchElementException as err:
            print 'No prime element:', err
        
        except StaleElementReferenceException as err:
            print 'Element is no longer attached to the DOM:', err

        except TimeoutException as err:
            print 'Timeout exception raised:', err

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
            except NoSuchElementException as err:
                print 'No breadcrumb category element:', err
            
            except StaleElementReferenceException as err:
                print 'Element is no longer attached to the DOM:', err

            # sub-category
            try:
                subcategory = breadcrumbs.find_element_by_css_selector('li:not(.a-breadcrumb-divider):nth-child(2) span.a-list-item').text
            except NoSuchElementException as err:
                print 'No breadcrumb sub-category element:', err
            
            except StaleElementReferenceException as err:
                print 'Element is no longer attached to the DOM:', err

            # description
            try:
                description = self.driver.find_element_by_css_selector('#productDescription').get_attribute('innerHTML')
            except NoSuchElementException as err:
                print 'No description element:', err
            
            except StaleElementReferenceException as err:
                print 'Element is no longer attached to the DOM:', err

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

                # images
                wait_forimage = WebDriverWait(self.driver, 10)
                wait_forimage.until(
                    EC.invisibility_of_element_located((By.CSS_SELECTOR, "#imageBlock li.a-spacing-small, #imageBlock li.item"))
                )

                image_list = []
                try:
                    image_list = self.driver.find_elements_by_css_selector('#imageBlock li.a-spacing-small, #imageBlock li.item')

                except NoSuchElementException as err:
                    print 'No image list element:', err
                
                except StaleElementReferenceException as err:
                    print 'Element is no longer attached to the DOM:', err

                for image_li in image_list:
                    try:
                        original_image_url = image_li.find_element_by_css_selector('img').get_attribute('src')
                        converted_picture_url = re.sub(settings.AMAZON_ITEM_IMAGE_CONVERT_PATTERN_FROM, settings.AMAZON_ITEM_IMAGE_CONVERT_STRING_TO, original_image_url)

                    except NoSuchElementException as err:
                        print 'No image url element:', err
                        continue
                    
                    except StaleElementReferenceException as err:
                        print 'Element is no longer attached to the DOM:', err
                        continue

                    try:
                        amazon_item_picture = AmazonItemPicture()
                        amazon_item_picture.amazon_item_id = amazon_item.id
                        amazon_item_picture.asin = amazon_item.asin
                        amazon_item_picture.original_picture_url = original_image_url
                        amazon_item_picture.converted_picture_url = converted_picture_url
                        amazon_item_picture.created_at = datetime.datetime.now()
                        amazon_item_picture.updated_at = datetime.datetime.now()

                        StormStore.add(amazon_item_picture)
                        StormStore.commit()
                     
                    except StormError as err:
                        print 'Image db insertion error:', err
                        continue

            else:
                print hyperlink + ' not matched'
        
        except NoSuchElementException as err:
            print 'No element:', err
        
        except StaleElementReferenceException as err:
            print 'Element is no longer attached to the DOM:', err

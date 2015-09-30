import sys, traceback
from os.path import basename
import datetime
import re
from decimal import Decimal

from pyvirtualdisplay import Display

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException

from storm.exceptions import StormError

from amazonmws import settings
from amazonmws import utils
from amazonmws.models import StormStore, AmazonItem, AmazonItemPicture, ScraperAmazonItem
from amazonmws.loggers import GrayLogger as logger

class AmazonItemDetailPageSpiderException(Exception):
    pass

class AmazonItemDetailPageSpider(object):

    page_opened = False
    url = None
    scraper_id = 0

    def __init__(self, url, scraper_id=1):
        # install phantomjs binary file - http://phantomjs.org/download.html
        # self.driver = webdriver.PhantomJS()

        # use firefox & vertual display instead. phantomjs cannot capture elements some cases.
        # ref: http://stackoverflow.com/a/23447450
        if 'linux' in sys.platform:
            self.display = Display(visible=0, size=(1280, 800))
            self.display.start()
        self.driver = webdriver.Firefox()
        self.page_opened = True
        self.url = url
        self.scraper_id = scraper_id

    def __del__(self):
        self.__quit()

    def __quit(self):
        if self.driver:
            self.driver.quit()
        if 'linux' in sys.platform and self.display:
            self.display.stop()

        self.page_opened = False

    def __conditions(self):
        is_fba = self.__is_FBA()

        if not is_fba:
            logger.info("[" + basename(__file__) + "] " + self.url + " NOT FBA")
            return False

        does_meet_extra_conditions = self.__extra_conditions()
        
        if not does_meet_extra_conditions:
            logger.info("[" + basename(__file__) + "] " + self.url + " NOT MEET EXTRA CONDITIONS")

        return is_fba and does_meet_extra_conditions

    def __is_FBA(self):

        is_fba = False

        try:
            wait = WebDriverWait(self.driver, 10)
            is_fba = wait.until(
                EC.presence_of_element_located((By.ID, "bbop-check-box"))
            )

        except NoSuchElementException:
            logger.exception('No prime element')
        
        except StaleElementReferenceException, e:
            logger.exception(e)

        except TimeoutException, e:
            logger.exception(e)

        return is_fba

    def __extra_conditions(self):
        """override this method
        """
        return True

    def load(self):
        self.driver.get(self.url)

        does_meet_conditions = False

        does_meet_conditions = self.__conditions()

        if does_meet_conditions != False:
            self.__parse()

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
                logger.exception('No breadcrumb category element')
            
            except StaleElementReferenceException, e:
                logger.exception(e)

            # sub-category
            try:
                subcategory = breadcrumbs.find_element_by_css_selector('li:not(.a-breadcrumb-divider):nth-child(2) span.a-list-item').text

            except NoSuchElementException:
                logger.exception('No breadcrumb sub-category element')
            
            except StaleElementReferenceException, e:
                logger.exception(e)

            # description
            ## remove .disclaim sections first
            js = "var els=document.getElementsByClassName('disclaim'); for (i=0;i<els.length;i++) { els[i].parentNode.removeChild(els[i]); }"
            self.driver.execute_script(js)

            description = None

            try:
                description = self.driver.find_element_by_css_selector('#productDescription').get_attribute('innerHTML')

            except NoSuchElementException:
                longer.exception('No description element')
            
            except StaleElementReferenceException, e:
                longer.exception(e)

            if description == None:

                try:
                    description = self.driver.find_element_by_css_selector('#descriptionAndDetails').get_attribute('innerHTML')

                except NoSuchElementException:
                    logger.exception('No description element')
                
                except StaleElementReferenceException, e:
                    logger.exception(e)

            summary_section = self.driver.find_element_by_css_selector('#centerCol')
            title = summary_section.find_element_by_css_selector('h1#title').text

            # price
            price = None
            
            try:
                price = summary_section.find_element_by_css_selector('#priceblock_ourprice')

            except NoSuchElementException:
                logger.exception('No price element')
            
            except StaleElementReferenceException, e:
                logger.exception(e)

            if price:
                price = Decimal(price.text.strip()[1:]).quantize(Decimal('1.00'))

            hyperlink = self.url
            match = re.match(settings.AMAZON_ITEM_LINK_PATTERN, hyperlink)

            if match:

                try:
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
                    amazon_item.status = AmazonItem.STATUS_ACTIVE
                    amazon_item.created_at = datetime.datetime.now()
                    amazon_item.updated_at = datetime.datetime.now()

                    StormStore.add(amazon_item)
                    StormStore.commit()

                except StormError, e:
                    logger.exception('AmazonItem db insertion error')
                    StormStore.rollback()
                    raise AmazonItemDetailPageSpiderException('AmazonItem db insertion error:', e)

                # scraper_amazon_items
                try:
                    scraper_amazon_item = ScraperAmazonItem()
                    scraper_amazon_item.scraper_id = self.scraper_id
                    scraper_amazon_item.amazon_item_id = amazon_item.id
                    scraper_amazon_item.asin = amazon_item.asin
                    scraper_amazon_item.created_at = datetime.datetime.now()
                    scraper_amazon_item.updated_at = datetime.datetime.now()

                    StormStore.add(scraper_amazon_item)
                    StormStore.commit()

                except StormError, e:
                    logger.exception('ScraperAmazonItem db insertion error')
                    StormStore.rollback()
                    raise AmazonItemDetailPageSpiderException('ScraperAmazonItem db insertion error:', e)

                # images
                try:
                    wait_forimage = WebDriverWait(self.driver, 10)
                    wait_forimage.until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "#imageBlock #altImages li.a-spacing-small, #imageBlock #altImages li.item"))
                    )

                except TimeoutException, e:
                    logger.exception(e)

                image_list = []
                try:
                    image_list = self.driver.find_elements_by_css_selector('#imageBlock #altImages li.a-spacing-small, #imageBlock #altImages li.item')

                except NoSuchElementException:
                    logger.exception('No image list element')
                
                except StaleElementReferenceException, e:
                    logger.exception(e)

                for image_li in image_list:
                    try:
                        original_image_url = image_li.find_element_by_css_selector('img').get_attribute('src')

                        image_already_exists = StormStore.find(AmazonItemPicture, AmazonItemPicture.original_picture_url == original_image_url, AmazonItemPicture.asin == amazon_item.asin).one()

                        if image_already_exists:
                            # image already exists in db
                            continue;

                        converted_picture_url = re.sub(settings.AMAZON_ITEM_IMAGE_CONVERT_PATTERN_FROM, settings.AMAZON_ITEM_IMAGE_CONVERT_STRING_TO, original_image_url)

                        # check the generated url is valid
                        is_converted_url_valid = utils.validate_url(converted_picture_url)

                        if not is_converted_url_valid:
                            continue

                    except NoSuchElementException:
                        logger.exception('No image url element')
                        continue
                    
                    except StaleElementReferenceException, e:
                        logger.exception(e)
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

                    except StormError:
                        logger.exception('AmazonItemPicture db insertion error')
                        continue

                StormStore.commit()

            else:
                logger.info("[" + basename(__file__) + "] " + hyperlink + " not matched")
        
        except NoSuchElementException:
            logger.exception("No element")
        
        except StaleElementReferenceException, e:
            logger.exception(e)

        except AmazonItemDetailPageSpiderException, e:
            logger.exception(e)

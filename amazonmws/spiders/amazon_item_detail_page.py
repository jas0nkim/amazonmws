import sys, traceback
from os.path import basename
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


class AmazonItemDetailPageSpiderException(Exception):
    pass

class AmazonItemDetailPageSpider(object):

    page_opened = False
    url = None
    task_id = 0
    asin = None

    def __init__(self, url, task_id=1):
        # install phantomjs binary file - http://phantomjs.org/download.html
        self.driver = webdriver.PhantomJS()

        # use firefox & vertual display instead. phantomjs cannot capture elements some cases.
        # ref: http://stackoverflow.com/a/23447450
        # if 'linux' in sys.platform:
        #     self.display = Display(visible=0, size=(1280, 800))
        #     self.display.start()
        # self.driver = webdriver.Firefox()
        self.page_opened = True
        self.url = url
        self.task_id = task_id
        logger.addFilter(StaticFieldFilter(get_logger_name(), Task.get_name(self.task_id)))

    def __del__(self):
        self.__quit()

    def __quit(self):
        if self.driver:
            self.driver.quit()
        # if 'linux' in sys.platform and self.display:
        #     self.display.stop()

        self.page_opened = False

    def __conditions(self):
        is_fba = AmazonItemDetailPageSpider.is_FBA(self.driver)

        if not is_fba:
            logger.info("[" + basename(__file__) + "] " + self.url + " NOT FBA")
            return False

        does_meet_extra_conditions = self.__extra_conditions()
        
        if not does_meet_extra_conditions:
            logger.info("[" + basename(__file__) + "] " + self.url + " NOT MEET EXTRA CONDITIONS")

        return is_fba and does_meet_extra_conditions

    @staticmethod
    def fba_presence_indicator(driver):
        element_text = driver.find_element_by_css_selector('#merchant-info').text.strip()
        return 'Ships from and sold by Amazon.com' in element_text or 'Fulfilled by Amazon' in element_text

    @staticmethod
    def is_FBA(driver):

        is_fba = False

        try:
            wait = WebDriverWait(driver, settings.APP_DEFAULT_WEBDRIVERWAIT_SEC)
            is_fba = wait.until(AmazonItemDetailPageSpider.fba_presence_indicator)

        except NoSuchElementException:
            logger.exception('No prime element')
        
        except StaleElementReferenceException, e:
            logger.exception(e)

        except TimeoutException:
            logger.exception("[" + driver.current_url + "] " + "CSS Selector Error: unable to find FBA element")

        return is_fba

    @staticmethod
    def get_price(driver):
        price = None

        try:
            # check deal price block first
            price = driver.find_element_by_css_selector('#priceblock_dealprice')

        except NoSuchElementException, e:
            logger.info("unable to find element with css #priceblock_dealprice")
        
        except StaleElementReferenceException, e:
            logger.exception(e)

        if price == None:
            try:
                # check sale price block second
                price = driver.find_element_by_css_selector('#priceblock_saleprice')

            except NoSuchElementException, e:
                logger.info("unable to find element with css #priceblock_saleprice")
            
            except StaleElementReferenceException, e:
                logger.exception(e)

        if price == None:
            # if no price block exists, check our price block
            try:
                price = driver.find_element_by_css_selector('#priceblock_ourprice')

            except NoSuchElementException, e:
                logger.info("unable to find element with css #priceblock_ourprice")
            
            except StaleElementReferenceException, e:
                logger.exception(e)

        if price:
            price = Decimal(price.text.strip()[1:]).quantize(Decimal('1.00'))

        else:
            raise AmazonItemDetailPageSpiderException("Unable to find any price element from this item")

        return price

    def __extra_conditions(self):
        """override this method
        """
        return True

    def load(self):

        match = re.match(settings.AMAZON_ITEM_LINK_PATTERN, self.url)
        
        if not match:
            logger.error("[" + self.url + "] " + "url not matched with amazon item link pattern")
            self.__quit()
            return False

        else:
            self.url = match.group(0)
            self.asin = match.group(3)

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

            try:
                breadcrumbs = self.driver.find_element_by_css_selector('#wayfinding-breadcrumbs_container ul')

            except NoSuchElementException:
                logger.exception("[ASIN: " + self.asin + "] " + "No breadcrumbs element")
            
            except StaleElementReferenceException, e:
                logger.exception(e)


            # category
            try:
                category = breadcrumbs.find_element_by_css_selector('li:not(.a-breadcrumb-divider):first-child span.a-list-item').text

            except NoSuchElementException:
                logger.exception("[ASIN: " + self.asin + "] " + "No breadcrumb category element")
            
            except StaleElementReferenceException, e:
                logger.exception(e)

            # sub-category
            try:
                subcategory = breadcrumbs.find_element_by_css_selector('li:not(.a-breadcrumb-divider):nth-child(2) span.a-list-item').text

            except NoSuchElementException:
                logger.exception("[ASIN: " + self.asin + "] " + "No breadcrumb sub-category element")
            
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
                logger.exception("[ASIN: " + self.asin + "] " + "No description element")
            
            except StaleElementReferenceException, e:
                logger.exception(e)

            if description == None:

                try:
                    description = self.driver.find_element_by_css_selector('#descriptionAndDetails').get_attribute('innerHTML')

                except NoSuchElementException:
                    logger.exception("[ASIN: " + self.asin + "] " + "No description element")
                
                except StaleElementReferenceException, e:
                    logger.exception(e)

            summary_section = self.driver.find_element_by_css_selector('#centerCol')
            title = summary_section.find_element_by_css_selector('h1#title').text

            # price
            price = None
            try:
                price = AmazonItemDetailPageSpider.get_price(self.driver)

            except AmazonItemDetailPageSpiderException:
                logger.exception("[ASIN: " + self.asin + "] " + "No price element can found")

            # review count & average rating
            review_count = None
            avg_rating = None

            try:
                review_count = int(self.driver.find_element_by_css_selector('#summaryStars').text.strip())

            except NoSuchElementException:
                logger.exception("[ASIN: " + self.asin + "] " + "No review count element")
            
            except StaleElementReferenceException, e:
                logger.exception(e)

            try:
                avg_rating = float(self.driver.find_element_by_css_selector('#avgRating').text.strip('out of 5 stars').strip())

            except NoSuchElementException:
                logger.exception("[ASIN: " + self.asin + "] " + "No average rating element")
            
            except StaleElementReferenceException, e:
                logger.exception(e)

            try:
                amazon_item = AmazonItem()
                amazon_item.url = self.url
                amazon_item.asin = self.asin
                if category:
                    amazon_item.category = category
                if subcategory:
                    amazon_item.subcategory = subcategory
                amazon_item.title = title
                amazon_item.price = price
                if description:
                    amazon_item.description = description.strip()
                if review_count:
                    amazon_item.review_count = review_count
                if avg_rating:
                    amazon_item.avg_rating = avg_rating
                amazon_item.status = AmazonItem.STATUS_ACTIVE
                amazon_item.created_at = datetime.datetime.now()
                amazon_item.updated_at = datetime.datetime.now()

                StormStore.add(amazon_item)
                StormStore.commit()

            except StormError, e:
                logger.exception("[ASIN: " + self.asin + "] " + "AmazonItem db insertion error")
                StormStore.rollback()
                raise AmazonItemDetailPageSpiderException('AmazonItem db insertion error:', e)

            # scraper_amazon_items
            try:
                scraper_amazon_item = ScraperAmazonItem()
                scraper_amazon_item.scraper_id = self.task_id
                scraper_amazon_item.amazon_item_id = amazon_item.id
                scraper_amazon_item.asin = amazon_item.asin
                scraper_amazon_item.created_at = datetime.datetime.now()
                scraper_amazon_item.updated_at = datetime.datetime.now()

                StormStore.add(scraper_amazon_item)
                StormStore.commit()

            except StormError, e:
                logger.exception("[ASIN: " + self.asin + "] " + "ScraperAmazonItem db insertion error")
                StormStore.rollback()
                raise AmazonItemDetailPageSpiderException('ScraperAmazonItem db insertion error:', e)

            # images
            try:
                wait_forimage = WebDriverWait(self.driver, settings.APP_DEFAULT_WEBDRIVERWAIT_SEC)
                wait_forimage.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "#imageBlock #altImages li.a-spacing-small, #imageBlock #altImages li.item"))
                )

            except TimeoutException, e:
                logger.exception(e)

            image_list = []
            try:
                image_list = self.driver.find_elements_by_css_selector('#imageBlock #altImages li.a-spacing-small, #imageBlock #altImages li.item')

            except NoSuchElementException:
                logger.exception("[ASIN: " + self.asin + "] " + "No image list element")
            
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
                    logger.exception("[ASIN: " + self.asin + "] " + "No image url element")
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
                    logger.exception("[ASIN: " + self.asin + "] " + "AmazonItemPicture db insertion error")
                    continue

            try:
                StormStore.commit()

            except StormError:
                logger.exception("[ASIN: " + self.asin + "] " + "Unable to commit data insertions")
        
        except AmazonItemDetailPageSpiderException, e:
            logger.exception(e)

import sys, traceback, os
from os.path import basename
import datetime, time
import re
import json
from decimal import Decimal

# from pyvirtualdisplay import Display

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException

from storm.exceptions import StormError

import RAKE

from amazonmws import settings
from amazonmws import utils
from amazonmws.models import StormStore, AmazonItem, AmazonItemPicture, Scraper, Task, LookupAmazonItem
from amazonmws.loggers import GrayLogger as logger, StaticFieldFilter, get_logger_name


class AmazonItemDetailPageSpiderException(Exception):
    pass

class AmazonItemDetailPageSpider(object):

    url = None
    task_id = 0
    lookup_id = None
    asin = None

    def __init__(self, url, task_id=1, lookup_id=None):
        # install phantomjs binary file - http://phantomjs.org/download.html
        self.driver = webdriver.PhantomJS()

        # use firefox & vertual display instead. phantomjs cannot capture elements some cases.
        # ref: http://stackoverflow.com/a/23447450
        # if 'linux' in sys.platform:
        #     self.display = Display(visible=0, size=(1280, 800))
        #     self.display.start()
        # self.driver = webdriver.Firefox()
        self.url = url
        self.task_id = task_id
        self.lookup_id = lookup_id
        logger.addFilter(StaticFieldFilter(get_logger_name(), Task.get_name(self.task_id)))

    def __del__(self):
        self.__quit()

    def __quit(self):
        if self.driver:
            self.driver.quit()
        # if 'linux' in sys.platform and self.display:
        #     self.display.stop()

    def __conditions(self):
        """ - check is FBA
            - check is out of stock (enough stock available)
        """
        is_fba = AmazonItemDetailPageSpider.is_FBA(self.driver)

        if not is_fba:
            logger.info("[url:" + self.url + "] " + "NOT FBA")
            return False

        has_enough_stock = AmazonItemDetailPageSpider.has_enough_stock(self.driver)

        if not has_enough_stock:
            logger.info("[url:" + self.url + "] " + "FBA but NOT ENOUGH STOCK")
            return False

        does_meet_extra_conditions = self.__extra_conditions()
        
        if not does_meet_extra_conditions:
            logger.info("[url:" + self.url + "] " + "FBA but NOT MEET EXTRA CONDITIONS")

        return is_fba and has_enough_stock and does_meet_extra_conditions

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
            logger.exception("[" + driver.current_url + "] " + "Unable to find FBA element")

        is_addon = AmazonItemDetailPageSpider.is_addon(driver)

        return is_fba and is_addon == False

    @staticmethod
    def is_addon(driver):
        is_addon = False

        try:
            wait = WebDriverWait(driver, settings.APP_DEFAULT_WEBDRIVERWAIT_SEC)
            is_addon = wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '#addOnItem_feature_div i.a-icon-addon'))
            )

        except NoSuchElementException:
            logger.exception('No addon icon element')
        
        except StaleElementReferenceException, e:
            logger.exception(e)

        except TimeoutException:
            logger.exception("[" + driver.current_url + "] " + "Unable to find FBA element")

        return is_addon

    @staticmethod
    def enough_stock_indicator(driver):
        element_text = driver.find_element_by_css_selector('#availability').text.strip().lower()
        return 'only' not in element_text and 'out' not in element_text

    @staticmethod
    def has_enough_stock(driver):
        has_enough_stock = False

        try:
            wait = WebDriverWait(driver, settings.APP_DEFAULT_WEBDRIVERWAIT_SEC)
            has_enough_stock = wait.until(AmazonItemDetailPageSpider.enough_stock_indicator)

        except NoSuchElementException:
            logger.exception('Not enough stock available')
        
        except StaleElementReferenceException, e:
            logger.exception(e)

        except TimeoutException:
            logger.exception("[" + driver.current_url + "] " + "Not enough stock available")

        return has_enough_stock

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

    @staticmethod
    def get_images(driver):
        ret = []

        html_source = driver.page_source
        m = re.search(r"'colorImages': \{(.+)\},\n", html_source)
        if m:
            # work with json
            json_dump = "{%s}" % m.group(1).replace('\'', '"')
            image_data = json.loads(json_dump)
            for key in image_data:
                images = image_data[key]
                for image in images:
                    if "hiRes" in image and image["hiRes"] != None:
                        ret.append(image["hiRes"])
                    elif "large" in image and image["large"] != None:
                        ret.append(image["large"])
                break
            return ret

        if len(ret) > 0:
            return ret

        else:
            # scrape manually
            try:
                wait = WebDriverWait(driver, settings.APP_DEFAULT_WEBDRIVERWAIT_SEC)
                image_li = wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '#main-image-container > ul li.image.item'))
                )
            except TimeoutException, e:
                logger.exception(e)
                return []

            try:
                original_image_url = image_li.find_element_by_css_selector('img').get_attribute('src')

                # try primary image url
                converted_picture_url = re.sub(settings.AMAZON_ITEM_IMAGE_CONVERT_PATTERN_FROM, settings.AMAZON_ITEM_IMAGE_CONVERT_STRING_TO_PRIMARY, original_image_url)
                if not utils.validate_url(converted_picture_url) or not utils.validate_image_size(converted_picture_url):
                    # try secondary image url
                    converted_picture_url = re.sub(settings.AMAZON_ITEM_IMAGE_CONVERT_PATTERN_FROM, settings.AMAZON_ITEM_IMAGE_CONVERT_STRING_TO_SECONDARY, original_image_url)
                    if not utils.validate_url(converted_picture_url) or not utils.validate_image_size(converted_picture_url):
                        ret.append(original_image_url)
                if len(ret) < 1:
                    ret.append(converted_picture_url)
                return ret

            except NoSuchElementException:
                logger.exception("No image url element")
                return []
            
            except StaleElementReferenceException, e:
                logger.exception(e)
                return []

    @staticmethod
    def get_reviewcount_and_avgrating(driver):
        review_count = None
        avg_rating = None

        try:
            # replace ','' to '' - in case of i.e. 1,000,000
            review_count = int(driver.find_element_by_css_selector('#summaryStars').text.strip().replace(',', ''))

        except NoSuchElementException:
            logger.exception("No review count element")
        
        except StaleElementReferenceException, e:
            logger.exception(e)

        try:
            avg_rating = float(driver.find_element_by_css_selector('#avgRating').text.strip('out of 5 stars').strip())

        except NoSuchElementException:
            logger.exception("No average rating element")
        
        except StaleElementReferenceException, e:
            logger.exception(e)

        return (review_count, avg_rating)

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
        features = None
        description = None

        try:
            # category
            try:
                breadcrumbs = self.driver.find_element_by_css_selector('#wayfinding-breadcrumbs_feature_div > ul')

            except NoSuchElementException:
                logger.exception("[ASIN: " + self.asin + "] " + "No breadcrumbs element")
            
            except StaleElementReferenceException, e:
                logger.exception(e)

            try:
                categories = []
                category_seq = breadcrumbs.find_elements_by_css_selector('li:not(.a-breadcrumb-divider) > span > a')
                if len(category_seq) > 0:
                    for category in category_seq:
                        categories.append(category.text.strip())
                    category = ' : '.join(categories)

            except NoSuchElementException:
                logger.exception("[ASIN: " + self.asin + "] " + "No breadcrumb category elements")
            
            except StaleElementReferenceException, e:
                logger.exception(e)

            # features
            try:
                features = self.driver.find_element_by_css_selector('#fbExpandableSectionContent').get_attribute('innerHTML')
            except NoSuchElementException:
                logger.exception("[ASIN: " + self.asin + "] " + "No features element")
            except StaleElementReferenceException, e:
                logger.exception(e)
            if features == None:
                try:
                    features = self.driver.find_element_by_css_selector('#feature-bullets').get_attribute('innerHTML')
                except NoSuchElementException:
                    logger.exception("[ASIN: " + self.asin + "] " + "No features element")
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

            # summary section
            summary_section = None            
            try:
                summary_section = self.driver.find_element_by_css_selector('#centerCol')
            except NoSuchElementException, e:
                logger.exception(e)
            except StaleElementReferenceException, e:
                logger.exception(e)

            if summary_section == None:            
                try:
                    summary_section = self.driver.find_element_by_css_selector('#leftCol')
                except NoSuchElementException, e:
                    logger.exception(e)
                except StaleElementReferenceException, e:
                    logger.exception(e)

            if summary_section == None:
                raise AmazonItemDetailPageSpiderException("[ASIN: " + self.asin + "] " + "No summary section available")

            title = None
            try:
                title = summary_section.find_element_by_css_selector('h1#title').text.strip()
            except NoSuchElementException, e:
                logger.exception(e)
            except StaleElementReferenceException, e:
                logger.exception(e)

            if title == None:
                raise AmazonItemDetailPageSpiderException("[ASIN: " + self.asin + "] " + "No title can found")


            # price
            price = None
            try:
                price = AmazonItemDetailPageSpider.get_price(self.driver)

            except AmazonItemDetailPageSpiderException:
                logger.exception("[ASIN: " + self.asin + "] " + "No price element can found")

            if price == None:
                raise AmazonItemDetailPageSpiderException("[ASIN: " + self.asin + "] " + "No price can found")

            # images
            image_list = AmazonItemDetailPageSpider.get_images(self.driver)
            if len(image_list) < 1:
                raise AmazonItemDetailPageSpiderException("[ASIN: " + self.asin + "] " + "No image can found")

            # review count & average rating
            (review_count, avg_rating) = AmazonItemDetailPageSpider.get_reviewcount_and_avgrating(self.driver)

            # ebay_category_id
            ebay_category_id = None
            # RAKE
            Rake = RAKE.Rake(os.path.join(settings.APP_PATH, 'rake', 'stoplists', 'SmartStoplist.txt'));
            # search with category
            if category != None:
                keywords = Rake.run(re.sub(r'([^\s\w]|_)+', ' ', category));
                if len(keywords) > 0:
                    ebay_category_id = utils.find_ebay_category_id(keywords[0][0], self.asin)

            if ebay_category_id < 0:
                # search again with title
                if title != None:
                    keywords = Rake.run(re.sub(r'([^\s\w]|_)+', ' ', title));
                    if len(keywords) > 0:
                        ebay_category_id = utils.find_ebay_category_id(keywords[0][0], self.asin)

                if ebay_category_id < 0:
                    logger.error("[ASIN: " + self.asin + "] " + "No ebay category found")
                    ebay_category_id = None

            try:
                amazon_item = AmazonItem()
                amazon_item.url = self.url
                amazon_item.asin = self.asin
                if category:
                    amazon_item.category = category
                amazon_item.title = title
                amazon_item.price = price
                if features:
                    amazon_item.features = features.strip()
                if description:
                    amazon_item.description = description.strip()
                if review_count:
                    amazon_item.review_count = review_count
                if avg_rating:
                    amazon_item.avg_rating = avg_rating
                if ebay_category_id:
                    amazon_item.ebay_category_id = ebay_category_id
                amazon_item.status = AmazonItem.STATUS_ACTIVE
                amazon_item.created_at = datetime.datetime.now()
                amazon_item.updated_at = datetime.datetime.now()

                StormStore.add(amazon_item)
                StormStore.commit()

                # find ebay category id

            except StormError, e:
                logger.exception("[ASIN: " + self.asin + "] " + "AmazonItem db insertion error")
                StormStore.rollback()
                raise AmazonItemDetailPageSpiderException('AmazonItem db insertion error:', e)

            if self.lookup_id:
                try:
                    lookup_amazon_item = LookupAmazonItem()
                    lookup_amazon_item.lookup_id = self.lookup_id
                    lookup_amazon_item.amazon_item_id = amazon_item.id
                    lookup_amazon_item.created_at = datetime.datetime.now()
                    lookup_amazon_item.updated_at = datetime.datetime.now()

                    StormStore.add(lookup_amazon_item)
                    StormStore.commit()

                except StormError, e:
                    logger.exception("[ASIN: " + self.asin + "] " + "LookupAmazonItem db insertion error")
                    StormStore.rollback()
                    raise AmazonItemDetailPageSpiderException('LookupAmazonItem db insertion error:', e)

            # images
            for image_url in image_list:
                try:
                    amazon_item_picture = AmazonItemPicture()
                    amazon_item_picture.amazon_item_id = amazon_item.id
                    amazon_item_picture.asin = amazon_item.asin
                    amazon_item_picture.original_picture_url = image_url
                    amazon_item_picture.converted_picture_url = image_url
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

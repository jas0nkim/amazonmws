import sys, os

sys.path.append('%s/../../' % os.path.dirname(__file__))

import re
import datetime
import uuid
import json

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException


from storm.exceptions import StormError

from ebaysdk.trading import Connection as Trading
from ebaysdk.exception import ConnectionError

from amazonmws import settings, utils
from amazonmws.models import StormStore, AmazonItem, AmazonItemPicture, Scraper, EbayItem, ItemPriceHistory, ItemStatusHistory, Task, EbayStore, LookupAmazonItem, Lookup, LookupOwnership
from amazonmws.spiders.amazon_item_detail_page import AmazonItemDetailPageSpider, AmazonItemDetailPageSpiderException
from amazonmws.spiders.amazon_item_offer_listing_page import AmazonItemOfferListingPageSpider, AmazonItemOfferListingPageSpiderException
from amazonmws.ebaystore.listing import ListingHandler
from amazonmws.errors import record_trade_api_error
from amazonmws.loggers import GrayLogger as logger, StaticFieldFilter, get_logger_name
from amazonmws.ebayapi.request_objects import generate_revise_inventory_status_obj


class UrgentUpdateAmazonPictures(object):
    amazon_item = None
    driver = None

    def __init__(self, amazon_item):
        self.amazon_item = amazon_item
        self.driver = webdriver.PhantomJS()

    def __del__(self):
        self.__quit()

    def __quit(self):
        if self.driver:
            self.driver.quit()

    def run(self):
        logger.info("[ASIN: " + self.amazon_item.asin + "] " + "start updating pictures...")
        print "[ASIN: " + self.amazon_item.asin + "] " + "start updating pictures..."

        amazon_item_url = settings.AMAZON_ITEM_LINK_FORMAT % self.amazon_item.asin
        self.driver.get(amazon_item_url)
        return self.__process()
        

    def __process(self):
        images = AmazonItemDetailPageSpider.get_images(self.driver)
        print images

        if len(images) < 1:
            logger.info("[" + self.amazon_item.asin + "] " + "No image found")
            return False

        # 1. remove already exists
        images_already_exists = StormStore.find(AmazonItemPicture, 
            AmazonItemPicture.asin == self.amazon_item.asin)

        removed_images = 0
        if images_already_exists.count() > 0:
            for image_already_exists in images_already_exists:
                original_picture_url = image_already_exists.original_picture_url
                StormStore.remove(image_already_exists)
                logger.info("[" + self.amazon_item.asin + "][" + original_picture_url + "] " + "image removed")
                removed_images += 1

        # 2. add image
        added_images = 0
        for image_url in images:
            try:
                amazon_item_picture = AmazonItemPicture()
                amazon_item_picture.amazon_item_id = self.amazon_item.id
                amazon_item_picture.asin = self.amazon_item.asin
                amazon_item_picture.original_picture_url = image_url
                amazon_item_picture.converted_picture_url = image_url
                amazon_item_picture.created_at = datetime.datetime.now()
                amazon_item_picture.updated_at = datetime.datetime.now()

                StormStore.add(amazon_item_picture)
                logger.info("[" + self.amazon_item.asin + "][" + image_url + "] " + "image added")
                added_images += 1

            except StormError:
                logger.exception("[ASIN: " + self.amazon_item.asin + "] " + "AmazonItemPicture db insertion error")
                continue

        if added_images > 0 or removed_images > 0:
            StormStore.commit()
            return True
        return False

if __name__ == "__main__":
    num_updated = 0
    logger.info("Amazon items pictures urgent updating started...")

    amazon_items = StormStore.find(AmazonItem)
    for amazon_item in amazon_items:
        ebay_item = None
        try:
            ebay_item = StormStore.find(EbayItem,
                EbayItem.amazon_item_id == amazon_item.id)

        except StormError:
            continue

        if ebay_item.count() > 0:
            continue

        else:
            logger.info("[" + amazon_item.asin + "] " + "Updating pictures")
            update = UrgentUpdateAmazonPictures(amazon_item)
            if update.run():
                num_updated += 1

    logger.info(str(num_updated) + " Amazon pictures updated")

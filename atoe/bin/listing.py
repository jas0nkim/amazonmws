import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'scrapers', 'amzn'))

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging

from amazonmws import settings as amazonmws_settings, utils as amazonmws_utils
from amazonmws.loggers import GrayLogger as logger

from atoe.actions import EbayItemAction
from atoe.models import *


class ListingHandler(object):

    ebay_store = None
    # max_num_listing = None
    
    __min_review_count = 10
    __asins_exclude = []

    # 
    # amazon to ebay category mapping dictionary
    #
    # e.g. {'Cell Phones & Accessories : Accessories : Car Accessories : Car Cradles & Mounts': 35190,
    #   'Electronics : Car & Vehicle Electronics : Marine Electronics : Marine GPS Accessories': 39754,
    #   'Automotive : Interior Accessories : Consoles & Organizers : Dash-Mounted Holders': 33695,
    #   ...
    #   }
    __atemap = {}

    def __init__(self, ebay_store, **kwargs):
        self.ebay_store = ebay_store
        if 'min_review_count' in kwargs:
            self.__min_review_count = kwargs['min_review_count']
        if 'asins_exclude' in kwargs:
            self.__asins_exclude = kwargs['asins_exclude']
        
        cmap = AtoECategoryMapModelManager.fetch()
        self.__atemap = { m.amazon_category:m.ebay_category_id for m in cmap }

    def __list_to_ebay(self, amazon_item, ebay_item):
        action = EbayItemAction(ebay_store=self.ebay_store,
                    amazon_item=amazon_item,
                    ebay_item=ebay_item)
        category_id = self.__atemap[amazon_item.category]
        picture_urls = action.upload_pictures(StormStore.find(AmazonItemPicture, 
            AmazonItemPicture.asin == amazon_item.asin))
        eb_price = amazonmws_utils.calculate_profitable_price(amazon_item.price, self.ebay_store)
        ebid = action.add_item(category_id, picture_urls, eb_price)
        
        succeed = False
        maxed_out = action.maxed_out()
        if ebid:
            # store in database
            EbayItemModelManager.create(self.ebay_store, amazon_item.asin, ebid, category_id, eb_price)
            succeed = True
        return (succeed, maxed_out)

    def run(self):
        pref_cats = EbayStorePreferredCategoryModelManager.fetch(self.ebay_store)
        for pref_cat in pref_cats:
            count = 1
            items = AmazonItemModelManager.fetch_filtered(pref_cat, self.__min_review_count, asins_exclude=self.__asins_exclude)
            for amazon_item, ebay_item in items:
                if count > pref_cat.max_items:
                    break

                if amazon_item.category not in self.__atemap:
                    logger.error("[%s] No category id found in map data - %s" % (self.ebay_store.username, amazon_item.category))
                    continue

                succeed, maxed_out = self.__list_to_ebay(amazon_item, ebay_item)

                if succeed:
                    count += 1

                if maxed_out:
                    logger.info("[%s] STOP LISTING - REACHED EBAY ITEM LIST LIMITATION" % self.ebay_store.username)
                    break
        return True


if __name__ == "__main__":
    ebay_stores = EbayStoreModelManager.fetch()

    for ebay_store in ebay_stores:
        handler = ListingHandler(ebay_store)
        handler.run()

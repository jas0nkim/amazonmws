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
    __asins_exclude = None

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
        # if 'max_num_listing' in kwargs:
        #     self.max_num_listing = kwargs['max_num_listing']
        if 'asins_exclude' in kwargs:
            self.__asins_exclude = kwargs['asins_exclude']
        
        cmap = AtoECategoryMapModelManager.fetch()
        self.__atemap = { m.amazon_category:m.ebay_category_id for m in cmap }

    def run(self):
        items = AmazonItemModelManager.fetch_filtered()
        count = 0

        for (amazon_item, ebay_item) in items:
            if amazon_item.category not in self.__atemap:
                logger.error("[%s] No category id found in map data - %s" % (self.ebay_store.username, amazon_item.category))
                continue

            action = EbayItemAction(ebay_store=self.ebay_store,
                        amazon_item=amazon_item,
                        ebay_item=ebay_item)
            category_id = self.__atemap[amazon_item.category]
            picture_urls = action.upload_pictures(StormStore.find(AmazonItemPicture, 
                AmazonItemPicture.asin == amazon_item.asin))
            eb_price = amazonmws_utils.calculate_profitable_price(self.amazon_item.price, self.ebay_store)
            ebid = action.add_item(category_id, picture_urls, eb_price)
            
            if ebid:
                # store in database
                EbayItemModelManager.create(self.ebay_store, amazon_item.asin, ebid, category_id, eb_price)
                count += 1

            if isinstance(self.max_num_listing, int) and count > self.max_num_listing:
                logger.error("[" + self.ebay_store.username + "] " + "STOP LISTING - REACHED MAX NUMBER OF LISTING - " + str(self.max_num_listing))
                break

            if to_ebay.reached_ebay_limit:
                logger.error("[" + self.ebay_store.username + "] " + "STOP LISTING - REACHED EBAY ITEM LIST LIMITATION")
                break


        return True

    # def __filter_items(self):
    #     """filter amazon item by:
    #         - amazon active item
    #         - item which has not listed at ebay store
    #         - scraper (if applicable)

    #         return type: list
    #     """

    #     result = []
    #     try:
    #         filtered_items = StormStore.find(AmazonItem,
    #             LookupAmazonItem.amazon_item_id == AmazonItem.id,
    #             LookupOwnership.lookup_id == LookupAmazonItem.lookup_id,
    #             LookupOwnership.ebay_store_id == self.ebay_store.id,
    #             AmazonItem.status == AmazonItem.STATUS_ACTIVE,
    #             AmazonItem.review_count >= self.__min_review_count).order_by(Desc(AmazonItem.avg_rating), Desc(AmazonItem.review_count))
    #     except StormError:
    #         logger.exception('Unable to filter amazon items')

    #     # workaround solution - stupid but storm doesn't support outer join...
    #     # what it supposes to do - i.e.
    #     #   SELECT * FROM pets AS p 
    #     #       LEFT OUTER JOIN lost-pets AS lp
    #     #       ON p.name = lp.name
    #     #       WHERE lp.id IS NULL
    #     #       
    #     # ref: http://stackoverflow.com/a/369861
    #     num_items = 0

    #     for amazon_item in filtered_items:
    #         if isinstance(self.__asins_exclude, list) and len(self.__asins_exclude) > 0:
    #             if amazon_item.asin in self.__asins_exclude:
    #                 continue
    #         ebay_item = False
    #         try:
    #             ebay_item = StormStore.find(EbayItem, 
    #                 EbayItem.amazon_item_id == amazon_item.id,
    #                 EbayItem.ebay_store_id == self.ebay_store.id).one()
            
    #         except StormError:
    #             logger.exception("[ASIN:" + amazon_item.asin + "] " + "Error on finding item in ebay_items table")
    #             continue

    #         if not ebay_item:
    #             num_items += 1
    #             item_set = (amazon_item, None)
    #             result.append(item_set)
            
    #         elif ebay_item.status == EbayItem.STATUS_OUT_OF_STOCK:
    #             """add OOS ebay item - need to restock to ebay because it's been restocked on amazon!
    #             """
    #             num_items += 1
    #             item_set = (amazon_item, ebay_item)
    #             result.append(item_set)

    #     logger.info("[" + self.ebay_store.username + "] " + "Number of items to list on ebay: " + str(num_items) + " items")

    #     return result


if __name__ == "__main__":
    ebay_stores = EbayStoreModelManager.fetch()

    for ebay_store in ebay_stores:
        handler = ListingHandler(ebay_store)
        handler.run()

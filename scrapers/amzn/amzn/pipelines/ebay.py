import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))

import re
import RAKE

from amazonmws import settings as amazonmws_settings, utils as amazonmws_utils
from amazonmws.model_managers import *

from atoe.actions import EbayItemAction

from amzn.spiders.amazon_pricewatch import AmazonPricewatchSpider
from amzn.items import AmazonItem


class AtoECategoryMappingPipeline(object):
    def process_item(self, item, spider):
        if isinstance(spider, AmazonPricewatchSpider):
            return item

        if isinstance(item, AmazonItem): # AmazonItem (scrapy item)
            if item.get('category', None) != None:
                a_to_b_map = AtoECategoryMapModelManager.fetch_one(item.get('category'))
                if a_to_b_map == None:
                    ebay_category_id, ebay_category_name = self.__find_eb_cat_by_am_cat(item)
                    AtoECategoryMapModelManager.create(item.get('category'), ebay_category_id=ebay_category_id, ebay_category_name=ebay_category_name)
        return item

    def __find_eb_cat_by_am_cat(self, item):
        Rake = RAKE.Rake(os.path.join(amazonmws_settings.APP_PATH, 'rake', 'stoplists', 'SmartStoplist.txt'));
        category_route = [re.sub(r'([^\s\w]|_)+', ' ', c).strip() for c in item.get('category').split(':')]
        depth = len(category_route)
        while True:
            keywords = Rake.run(' '.join(category_route));
            if len(keywords) > 0:
                ebay_action = EbayItemAction()
                ebay_category_info = ebay_action.find_category(keywords[0][0])
                if not ebay_category_info and depth >= 4:
                    category_route = category_route[:-1]
                    depth -= 1
                else:
                    return ebay_category_info
            else:
                break
        return (None, None)


class EbayItemUpdatingPipeline(object):

    __exclude_store_ids = [ 3, ]

    def process_item(self, item, spider):
        if not isinstance(spider, AmazonPricewatchSpider):
            return item

        if isinstance(item, AmazonItem): # AmazonItem (scrapy item)
            a_item = AmazonItemModelManager.fetch_one(item.get('asin', ''))
            if not a_item:
                return item
            """ - check status
                - check is FBA
                - check is add-on
                - check quantity
                - check is price same
            """
            if not item.get('status'):
                self.__inactive_items(a_item.asin)
            if not item.get('is_fba'):
                self.__inactive_items(a_item.asin)
            if item.get('is_addon'):
                self.__inactive_items(a_item.asin)
            if item.get('quantity', 0) < amazonmws_settings.AMAZON_MINIMUM_QUANTITY_FOR_LISTING:
                self.__oos_items(a_item.asin)

            new_price = amazonmws_utils.number_to_dcmlprice(item.get('price'))
            if new_price != a_item.price:
                self.__update_prices(a_item.asin, new_price)
        return item

    def __inactive_items(self, asin):
        """inactive all ebay items have given asin
        """
        ebay_items = EbayItemModelManager.fetch(asin=asin)
        if ebay_items.count() > 0:
            for ebay_item in ebay_items:
                if ebay_item.ebay_store_id in self.__exclude_store_ids:
                    continue
                ebay_store = EbayStoreModelManager.fetch_one(id=ebay_item.ebay_store_id)
                if not ebay_store:
                    continue
                ebay_action = EbayItemAction(ebay_store=ebay_store, ebay_item=ebay_item)
                succeed = ebay_action.end_item()
                if succeed:
                    EbayItemModelManager.inactive(ebay_item)

    def __oos_items(self, asin):
        """make OOS all ebay items have given asin
        """
        ebay_items = EbayItemModelManager.fetch(asin=asin)
        if ebay_items.count() > 0:
            for ebay_item in ebay_items:
                if ebay_item.ebay_store_id in self.__exclude_store_ids:
                    continue
                ebay_store = EbayStoreModelManager.fetch_one(id=ebay_item.ebay_store_id)
                if not ebay_store:
                    continue
                ebay_action = EbayItemAction(ebay_store=ebay_store, ebay_item=ebay_item)
                succeed = ebay_action.revise_item(None, 0)
                if succeed:
                    EbayItemModelManager.oos(ebay_item)

    def __update_prices(self, asin, new_price):
        """update all ebay items have given asin
        """
        ebay_items = EbayItemModelManager.fetch(asin=asin)
        if ebay_items.count() > 0:
            for ebay_item in ebay_items:
                if ebay_item.ebay_store_id in self.__exclude_store_ids:
                    continue
                ebay_store = EbayStoreModelManager.fetch_one(id=ebay_item.ebay_store_id)
                if not ebay_store:
                    continue
                new_ebay_price = amazonmws_utils.calculate_profitable_price(new_price, ebay_store)
                ebay_action = EbayItemAction(ebay_store=ebay_store, ebay_item=ebay_item)
                succeed = ebay_action.revise_item(new_ebay_price, None)
                if succeed:
                    EbayItemModelManager.update_price(ebay_item, new_ebay_price)

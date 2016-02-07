import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'rfi'))

import re
import RAKE

from django.core.exceptions import MultipleObjectsReturned

from amazonmws import settings as amazonmws_settings, utils as amazonmws_utils
from amazonmws.model_managers import *

from atoe.actions import EbayItemAction

from amzn.spiders.amazon_pricewatch import AmazonPricewatchSpider
from amzn.items import AmazonItem

from rfi_listings.models import EbayItem


class AtoECategoryMappingPipeline(object):
    def process_item(self, item, spider):
        if isinstance(spider, AmazonPricewatchSpider):
            return item

        if isinstance(item, AmazonItem): # AmazonItem (scrapy item)
            if item.get('category', None) != None:
                a_to_b_map = AtoECategoryMapModelManager.fetch_one(item.get('category'))
                if a_to_b_map == None:
                    ebay_category_id, ebay_category_name = self.__find_eb_cat_by_am_cat(item)
                    AtoECategoryMapModelManager.create(amazon_category=item.get('category'), ebay_category_id=ebay_category_id, ebay_category_name=ebay_category_name)
        return item

    def __find_eb_cat_by_am_cat(self, item):
        Rake = RAKE.Rake(os.path.join(amazonmws_settings.APP_PATH, 'rake', 'stoplists', 'SmartStoplist.txt'));
        category_route = [re.sub(r'([^\s\w]|_)+', ' ', c).strip() for c in item.get('category').split(':')]
        _rand_ebay_store = EbayStoreModelManager.fetch_one(random=True)
        while True:
            depth = len(category_route)
            keywords = Rake.run(' '.join(category_route));
            if len(keywords) > 0:
                ebay_action = EbayItemAction(ebay_store=_rand_ebay_store)
                ebay_category_info = ebay_action.find_category(keywords[0][0])
                if not ebay_category_info and depth > 2:
                    del category_route[1] # remove the second in category route
                else:
                    if not ebay_category_info:
                        return (None, None)
                    return ebay_category_info
            else:
                break
        return (None, None)


class EbayItemUpdatingPipeline(object):

    __exclude_store_ids = [2, ]

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
                # self.__inactive_items(a_item.asin)
                self.__oos_items(a_item.asin)
                return item
            if not item.get('is_fba'):
                # self.__inactive_items(a_item.asin)
                self.__oos_items(a_item.asin)
                return item
            if item.get('is_addon'):
                # self.__inactive_items(a_item.asin)
                self.__oos_items(a_item.asin)
                return item
            if item.get('is_pantry'):
                # self.__inactive_items(a_item.asin)
                self.__oos_items(a_item.asin)
                return item
            if item.get('quantity', 0) < amazonmws_settings.AMAZON_MINIMUM_QUANTITY_FOR_LISTING:
                self.__oos_items(a_item.asin)
                return item

            self.__active_items_and_update_prices(a_item, item)
        return item

    def __inactive_items(self, asin):
        """inactive all ebay items have given asin
        """
        ebay_items = EbayItemModelManager.fetch(asin=asin)
        if ebay_items.count() > 0:
            for ebay_item in ebay_items:
                if ebay_item.ebay_store_id in self.__exclude_store_ids:
                    continue
                try:
                    ebay_store = ebay_item.ebay_store
                except MultipleObjectsReturned as e:
                    logger.exception("[EBID:%s] Multile ebay items exist" % ebay_item.ebid)
                    continue
                except EbayItem.DoesNotExist as e:
                    logger.exception("[EBID:%s] Failed to fetch an ebay item" % ebay_item.ebid)
                    continue
                if EbayItemModelManager.is_inactive(ebay_item): # already inactive item. do nothing
                    continue

                ebay_action = EbayItemAction(ebay_store=ebay_store, ebay_item=ebay_item)
                succeed = ebay_action.end_item()
                if succeed:
                    EbayItemModelManager.inactive(ebay_item=ebay_item)

    def __oos_items(self, asin):
        """make OOS all ebay items have given asin
        """
        ebay_items = EbayItemModelManager.fetch(asin=asin)
        if ebay_items.count() > 0:
            for ebay_item in ebay_items:
                if ebay_item.ebay_store_id in self.__exclude_store_ids:
                    continue
                try:
                    ebay_store = ebay_item.ebay_store
                except MultipleObjectsReturned as e:
                    logger.exception("[EBID:%s] Multile ebay items exist" % ebay_item.ebid)
                    continue
                except EbayItem.DoesNotExist as e:
                    logger.exception("[EBID:%s] Failed to fetch an ebay item" % ebay_item.ebid)
                    continue
                if EbayItemModelManager.is_oos(ebay_item): # already oos item. do nothing
                    continue
                
                ebay_action = EbayItemAction(ebay_store=ebay_store, ebay_item=ebay_item)
                succeed = ebay_action.revise_inventory(eb_price=None, quantity=0)
                if succeed:
                    EbayItemModelManager.oos(ebay_item)

    def __active_items_and_update_prices(self, amazon_item, item):
        """update all ebay items have given asin
        """
        ebay_items = EbayItemModelManager.fetch(asin=amazon_item.asin)
        if ebay_items.count() > 0:
            for ebay_item in ebay_items:
                if ebay_item.ebay_store_id in self.__exclude_store_ids:
                    continue
                try:
                    ebay_store = ebay_item.ebay_store
                except MultipleObjectsReturned as e:
                    logger.exception("[EBID:%s] Multile ebay items exist" % ebay_item.ebid)
                    continue
                except EbayItem.DoesNotExist as e:
                    logger.exception("[EBID:%s] Failed to fetch an ebay item" % ebay_item.ebid)
                    continue
                new_ebay_price = amazonmws_utils.calculate_profitable_price(amazonmws_utils.number_to_dcmlprice(item.get('price')), ebay_store)
                if ebay_item.eb_price == new_ebay_price and EbayItemModelManager.is_active(ebay_item) and amazon_item.title == item.get('title'):
                    continue

                ebay_action = EbayItemAction(ebay_store=ebay_store, ebay_item=ebay_item, amazon_item=amazon_item)
                if amazon_item.title != new_title:
                    succeed = ebay_action.revise_item(title=item.get('title'), description=item.get('description'), price=new_ebay_price, quantity=amazonmws_settings.EBAY_ITEM_DEFAULT_QUANTITY)
                else:
                    succeed = ebay_action.revise_inventory(eb_price=new_ebay_price, quantity=amazonmws_settings.EBAY_ITEM_DEFAULT_QUANTITY)
                if succeed:
                    EbayItemModelManager.update_price_and_active(ebay_item, new_ebay_price)

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'rfi'))

import re
import RAKE

from django.core.exceptions import MultipleObjectsReturned

from amazonmws import settings as amazonmws_settings, utils as amazonmws_utils
from amazonmws.model_managers import *

from atoe.actions import EbayItemAction
from atoe.helpers import CategoryHandler

from amzn.spiders.amazon_pricewatch import AmazonPricewatchSpider
from amzn.items import AmazonItem

from rfi_listings.models import EbayItem


class AtoECategoryMappingPipeline(object):
    """AmazonItem only pipeline
    """
    
    def process_item(self, item, spider):
        if isinstance(spider, AmazonPricewatchSpider):
            return item

        if isinstance(item, AmazonItem): # AmazonItem (scrapy item)
            amazon_category_breadcrumb = item.get('category', None)

            if not amazon_category_breadcrumb:
                return item

            a_to_b_map = AtoECategoryMapModelManager.fetch_one(amazon_category_breadcrumb)
            if a_to_b_map: # given amazon cagetory already exists in map table. skip it
                return item

            _rand_ebay_store = EbayStoreModelManager.fetch_one(random=True)
            handler = CategoryHandler(ebay_store=_rand_ebay_store)
            ebay_category_id, ebay_category_name = handler.find_ebay_category(amazon_category_breadcrumb)
            AtoECategoryMapModelManager.create(amazon_category=amazon_category_breadcrumb,
                ebay_category_id=ebay_category_id,
                ebay_category_name=ebay_category_name)

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
    """AmazonPricewatchSpider only pipeline
    """

    __exclude_store_ids = [2, 3, 4,]

    def process_item(self, item, spider):
        if not isinstance(spider, AmazonPricewatchSpider):
            return item

        if isinstance(item, AmazonItem): # AmazonItem (scrapy item)
            a_item = AmazonItemModelManager.fetch_one(item.get('asin', ''))
            if not a_item:
                return item
            """ - check status
                - check price is 0.00
                - check is FBA
                - check is add-on
                - check is pantry
                - check quantity
                - check is price same
            """
            if not item.get('status'):
                # self.__inactive_items(a_item.asin)
                self.__oos_items(amazon_item=a_item)
                return item
            if not float(item.get('price')) == 0.00:
                self.__oos_items(amazon_item=a_item)
                return item
            if not item.get('is_fba'):
                # self.__inactive_items(a_item.asin)
                self.__oos_items(amazon_item=a_item)
                return item
            if item.get('is_addon'):
                # self.__inactive_items(a_item.asin)
                self.__oos_items(amazon_item=a_item)
                return item
            if item.get('is_pantry'):
                # self.__inactive_items(a_item.asin)
                self.__oos_items(amazon_item=a_item)
                return item
            if item.get('quantity', 0) < amazonmws_settings.AMAZON_MINIMUM_QUANTITY_FOR_LISTING:
                self.__oos_items(amazon_item=a_item)
                return item

            self.__active_items_and_update_prices(amazon_item=a_item, item=item)
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
                if EbayItemModelManager.is_inactive(ebay_item): # already inactive (ended) item. do nothing
                    continue

                ebay_action = EbayItemAction(ebay_store=ebay_store, ebay_item=ebay_item)
                succeed = ebay_action.end_item()
                if succeed:
                    EbayItemModelManager.inactive(ebay_item=ebay_item)

    def __oos_items(self, amazon_item):
        """make OOS all ebay items have given asin
        """
        # if not amazon_item.is_listable(): # has not listed anyway. skip it.
        #     return False

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
                if EbayItemModelManager.is_inactive(ebay_item): # inactive (ended) item. do nothing
                    continue
                if EbayItemModelManager.is_oos(ebay_item): # already oos item. do nothing
                    continue
                
                ebay_action = EbayItemAction(ebay_store=ebay_store, ebay_item=ebay_item, amazon_item=amazon_item)
                succeed = ebay_action.revise_inventory(eb_price=None, quantity=0, revise_item=True)
                if succeed:
                    EbayItemModelManager.oos(ebay_item)

    def __update_price_necesary(self, amazon_item, item):
        if amazon_item.price == number_to_dcmlprice(item.get('price')):
            return False
        return True

    def __update_content_necesary(self, item):
        if item.get('is_title_changed'):
            return True
        return False

    def __active_items_and_update_prices(self, amazon_item, item):
        """update all ebay items have given asin
        """
        # if amazon_item.is_listable() and not self.__update_price_necesary(amazon_item=amazon_item, item=item) and not self.__update_content_necesary(amazon_item=amazon_item, item=item):
        #     return False

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
                if EbayItemModelManager.is_inactive(ebay_item): # inactive (ended) item. do nothing
                    continue

                new_ebay_price = amazonmws_utils.calculate_profitable_price(amazonmws_utils.number_to_dcmlprice(item.get('price')), ebay_store)

                ebay_action = EbayItemAction(ebay_store=ebay_store, ebay_item=ebay_item, amazon_item=amazon_item)
                succeed = ebay_action.revise_inventory(
                    eb_price=new_ebay_price,
                    quantity=amazonmws_settings.EBAY_ITEM_DEFAULT_QUANTITY,
                    revise_item=self.__update_content_necesary(item=item))

                if succeed:
                    EbayItemModelManager.update_price_and_active(ebay_item, new_ebay_price)

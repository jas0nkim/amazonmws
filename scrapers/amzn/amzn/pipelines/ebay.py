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

            a_to_b_map = AtoECategoryMapModelManager.fetch_one(amazon_category=amazon_category_breadcrumb)
            if a_to_b_map: # given amazon cagetory already exists in map table. skip it
                return item

            _rand_ebay_store = EbayStoreModelManager.fetch_one(random=True)
            handler = CategoryHandler(ebay_store=_rand_ebay_store)
            ebay_category_id, ebay_category_name = handler.find_ebay_category(amazon_category_breadcrumb)
            AtoECategoryMapModelManager.create(amazon_category=amazon_category_breadcrumb,
                ebay_category_id=ebay_category_id,
                ebay_category_name=ebay_category_name)
            category_features = handler.find_ebay_category_features(category_id=ebay_category_id)
            if category_features:
                ecf = EbayCategoryFeaturesModelManager.fetch_one(ebay_category_id=ebay_category_id)
                if ecf:
                    EbayCategoryFeaturesModelManager.update(feature=ecf,
                        upc_enabled=category_features.get('UPCEnabled', False),
                        variations_enabled=category_features.get('VariationsEnabled', False))
                else:
                    EbayCategoryFeaturesModelManager.create(ebay_category_id=ebay_category_id,
                        ebay_category_name=ebay_category_name,
                        upc_enabled=category_features.get('UPCEnabled', False),
                        variations_enabled=category_features.get('VariationsEnabled', False))
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
                    category_route.pop(1) # remove the second in category route
                else:
                    if not ebay_category_info:
                        return (None, None)
                    return ebay_category_info
            else:
                break
        return (None, None)


class EbayItemInventoryUpdatingPipeline(object):
    """AmazonPricewatchSpider only pipeline
    """

    __exclude_store_ids = [2, 3, 4,]

    def process_item(self, item, spider):
        if not isinstance(spider, AmazonPricewatchSpider):
            return item

        if isinstance(item, AmazonItem): # AmazonItem (scrapy item)
            self.__handle_redirected_asin(redirected_asins=item.get('_redirected_asins', {}))

            a_item = AmazonItemModelManager.fetch_one(asin=item.get('asin', ''))
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
                if a_item.is_a_variation():
                    self.__delete_variation(amazon_item=a_item)
                else:
                    self.__oos_items(amazon_item=a_item)
                return item
            if float(item.get('price')) == 0.00:
                self.__oos_items(amazon_item=a_item)
                return item
            if not item.get('is_fba'):
                self.__oos_items(amazon_item=a_item)
                return item
            if item.get('is_addon'):
                self.__oos_items(amazon_item=a_item)
                return item
            if item.get('is_pantry'):
                self.__oos_items(amazon_item=a_item)
                return item
            if item.get('quantity', 0) < amazonmws_settings.AMAZON_MINIMUM_QUANTITY_FOR_LISTING:
                self.__oos_items(amazon_item=a_item)
                return item

            self.__active_items_and_update_prices(amazon_item=a_item, item=item)
        return item

    def __oos_items(self, amazon_item, do_revise_item=False):
        """make OOS all ebay items/variations have given asin
        """
        ebay_item_variations = EbayItemVariationModelManager.fetch(asin=amazon_item.asin)
        if ebay_item_variations.count() > 0:
            for ebay_item_variation in ebay_item_variations:                
                try:
                    ebay_store = ebay_item_variation.ebay_item.ebay_store
                except Exception as e:
                    logger.exception("[EBID:%s] Unable to find ebay store" % ebay_item_variation.ebid)
                    continue

                if ebay_store.id in self.__exclude_store_ids:
                    continue
                if EbayItemModelManager.is_inactive(ebay_item_variation.ebay_item): # inactive (ended) item. do nothing
                    continue
                ebay_action = EbayItemAction(ebay_store=ebay_store, ebay_item=ebay_item_variation.ebay_item, amazon_item=amazon_item)
                succeed = ebay_action.revise_inventory(eb_price=None, 
                    quantity=0,
                    asin=amazon_item.asin)
                if succeed:
                    EbayItemVariationModelManager.oos(ebay_item_variation)

        ebay_items = EbayItemModelManager.fetch(asin=amazon_item.asin)
        if ebay_items.count() > 0:
            for ebay_item in ebay_items:
                try:
                    ebay_store = ebay_item.ebay_store
                except Exception as e:
                    logger.exception("[EBID:%s] Unable to find ebay store" % ebay_item.ebid)
                    continue

                if ebay_store.id in self.__exclude_store_ids:
                    continue
                if EbayItemModelManager.is_inactive(ebay_item): # inactive (ended) item. do nothing
                    continue
                if EbayItemModelManager.has_variations(ebay_item):
                    continue
                
                ebay_action = EbayItemAction(ebay_store=ebay_store, ebay_item=ebay_item, amazon_item=amazon_item)
                succeed = ebay_action.revise_inventory(eb_price=None,
                    quantity=0,
                    do_revise_item=do_revise_item)
                if succeed:
                    EbayItemModelManager.oos(ebay_item)

    def __delete_variation(self, amazon_item):
        """remove all ebay variations have given asin
        """
        ebay_item_variations = EbayItemVariationModelManager.fetch(asin=amazon_item.asin)
        if ebay_item_variations.count() > 0:
            for ebay_item_variation in ebay_item_variations:
                try:
                    ebay_store = ebay_item_variation.ebay_item.ebay_store
                except Exception as e:
                    logger.exception("[EBID:%s] Unable to find ebay store" % ebay_item_variation.ebid)
                    continue

                if ebay_store.id in self.__exclude_store_ids:
                    continue
                if EbayItemModelManager.is_inactive(ebay_item_variation.ebay_item): # inactive (ended) item. do nothing
                    continue
                ebay_action = EbayItemAction(ebay_store=ebay_store, ebay_item=ebay_item_variation.ebay_item, amazon_item=amazon_item)
                succeed = ebay_action.delete_variations(variations=
                    { 'Variation': [
                        {'Delete': True, 'SKU': amazon_item.asin }
                    ]})
                if succeed:
                    EbayItemVariationModelManager.delete(ebid=ebay_item_variation.ebid,
                        asin__in=[amazon_item.asin, ])

    def __update_price_necesary(self, amazon_item, item):
        if amazon_item.price == number_to_dcmlprice(item.get('price')):
            return False
        return True

    def __update_content_necesary(self, amazon_item, item):
        if amazon_item.title != item.get('title'):
            return True
        return False

    def __active_items_and_update_prices(self, amazon_item, item):
        """update all ebay items/variations have given asin
        """
        ebay_item_variations = EbayItemVariationModelManager.fetch(asin=amazon_item.asin)
        if ebay_item_variations.count() > 0:
            for ebay_item_variation in ebay_item_variations:
                try:
                    ebay_store = ebay_item_variation.ebay_item.ebay_store
                except Exception as e:
                    logger.exception("[EBID:%s] Unable to find ebay store" % ebay_item_variation.ebid)
                    continue

                if ebay_store.id in self.__exclude_store_ids:
                    continue
                if EbayItemModelManager.is_inactive(ebay_item_variation.ebay_item): # inactive (ended) item. do nothing
                    continue

                amazon_price = amazonmws_utils.number_to_dcmlprice(item.get('price'))
                new_ebay_price = None
                if amazon_price > 1:
                    new_ebay_price = amazonmws_utils.calculate_profitable_price(amazon_price, ebay_store)

                ebay_action = EbayItemAction(ebay_store=ebay_store, ebay_item=ebay_item_variation.ebay_item, amazon_item=amazon_item)
                succeed = ebay_action.revise_inventory(eb_price=new_ebay_price, 
                    quantity=amazonmws_settings.EBAY_ITEM_DEFAULT_QUANTITY,
                    asin=amazon_item.asin)
                if succeed:
                    EbayItemVariationModelManager.update_price_and_active(variation=ebay_item_variation,
                        eb_price=new_ebay_price,
                        quantity=amazonmws_settings.EBAY_ITEM_DEFAULT_QUANTITY)

        ebay_items = EbayItemModelManager.fetch(asin=amazon_item.asin)
        if ebay_items.count() > 0:
            for ebay_item in ebay_items:
                try:
                    ebay_store = ebay_item.ebay_store
                except Exception as e:
                    logger.exception("[EBID:%s] Unable to find ebay store" % ebay_item.ebid)
                    continue
                
                if ebay_store.id in self.__exclude_store_ids:
                    continue
                if EbayItemModelManager.is_inactive(ebay_item): # inactive (ended) item. do nothing
                    continue
                if EbayItemModelManager.has_variations(ebay_item):
                    continue

                amazon_price = amazonmws_utils.number_to_dcmlprice(item.get('price'))
                new_ebay_price = None
                if amazon_price > 1:
                    new_ebay_price = amazonmws_utils.calculate_profitable_price(amazon_price, ebay_store)

                ebay_action = EbayItemAction(ebay_store=ebay_store, ebay_item=ebay_item, amazon_item=amazon_item)
                succeed = ebay_action.revise_inventory(eb_price=new_ebay_price,
                    quantity=amazonmws_settings.EBAY_ITEM_DEFAULT_QUANTITY)
                if succeed:
                    EbayItemModelManager.update_price_and_active(ebay_item, new_ebay_price)

    def __handle_redirected_asin(self, redirected_asins):
        """ make OOS if any redrected asin (not the same as end-point/final asin)
        """
        if len(redirected_asins) > 0:
            for r_asin in redirected_asins.values():
                try:
                    ra_item = AmazonItemModelManager.fetch_one(r_asin)
                    if not ra_item:
                        continue
                    if ra_item.is_a_variation():
                        self.__delete_variation(amazon_item=ra_item)
                    else:
                        self.__oos_items(amazon_item=ra_item)
                except Exception as e:
                    logger.exception("[ASIN:%s] Failed to set out-of-stock a redirected amazon item or variation (asin)" % r_asin)
                    continue
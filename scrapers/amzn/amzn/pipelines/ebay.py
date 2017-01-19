import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'rfi'))

import re
import RAKE

from django.core.exceptions import MultipleObjectsReturned

from amazonmws import settings as amazonmws_settings, utils as amazonmws_utils
from amazonmws.model_managers import *

from atoe.helpers import CategoryHandler, ListingHandler

from amzn.spiders import *
from amzn.items import AmazonItem

from rfi_listings.models import EbayItem


class AmazonToEbayCategoryMapPipeline(object):
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
                        variations_enabled=amazonmws_utils.convertEbayApiBooleanValue(category_features.get('VariationsEnabled', False)))
                else:
                    EbayCategoryFeaturesModelManager.create(ebay_category_id=ebay_category_id,
                        ebay_category_name=ebay_category_name,
                        upc_enabled=category_features.get('UPCEnabled', False),
                        variations_enabled=amazonmws_utils.convertEbayApiBooleanValue(category_features.get('VariationsEnabled', False)))
        return item

    ###############
    # Deprecated
    ###############
    #
    # def __find_eb_cat_by_am_cat(self, item):
    #     Rake = RAKE.Rake(os.path.join(amazonmws_settings.APP_PATH, 'rake', 'stoplists', 'SmartStoplist.txt'));
    #     category_route = [re.sub(r'([^\s\w]|_)+', ' ', c).strip() for c in item.get('category').split(':')]
    #     _rand_ebay_store = EbayStoreModelManager.fetch_one(random=True)
    #     while True:
    #         depth = len(category_route)
    #         keywords = Rake.run(' '.join(category_route));
    #         if len(keywords) > 0:
    #             ebay_action = EbayItemAction(ebay_store=_rand_ebay_store)
    #             ebay_category_info = ebay_action.find_category(keywords[0][0])
    #             if not ebay_category_info and depth > 2:
    #                 category_route.pop(1) # remove the second in category route
    #             else:
    #                 if not ebay_category_info:
    #                     return (None, None)
    #                 return ebay_category_info
    #         else:
    #             break
    #     return (None, None)


class EbayItemListingPipeline(object):

    __ebay_store = None
    __task_id = None
    __maxed_out = False

    __cached_asins = {}
    __cached_ebids = {}

    def __do_list(self, handler, parent_asin):
        amazon_items = AmazonItemModelManager.fetch_its_variations(parent_asin=parent_asin)
        ebay_item = EbayItemModelManager.fetch_one(ebay_store_id=self.__ebay_store.id, asin=parent_asin)
        succeed, maxed_out = handler.run_each(amazon_items=amazon_items, ebay_item=ebay_item)
        if maxed_out:
            self.__maxed_out = maxed_out
        return succeed

    def __do_sync(self, handler, ebay_item):
        return handler.sync_item(ebay_item=ebay_item)

    def __do_revise(self, handler, ebay_item):
        success, maxed_out = handler.revise_item(ebay_item=ebay_item)
        if maxed_out:
            self.__maxed_out = maxed_out
        return success

    def __do_revise_inventory(self, handler, ebay_item):
        return handler.revise_inventory(ebay_item=ebay_item)

    def __start_ebay_listing(self, list_new=False, revise_inventory_only=False):
        # list to ebay store
        handler = ListingHandler(ebay_store=self.__ebay_store)

        # find all amazon items (asin) have same parent_asin
        for t in amazonmws_utils.queryset_iterator(AmazonScrapeTaskModelManager.fetch(task_id=self.__task_id, ebay_store_id=self.__ebay_store.id)):
            if list_new:
                if t.parent_asin not in self.__cached_asins:
                    self.__do_list(handler=handler, parent_asin=t.parent_asin)
                    self.__cached_asins[t.parent_asin] = True
            else:
                e_item = EbayItemModelManager.fetch_one(ebay_store_id=self.__ebay_store.id, asin=t.parent_asin)
                if e_item and e_item.ebid not in self.__cached_ebids:
                    self.__cached_ebids[e_item.ebid] = True
                    e_item = self.__do_sync(handler=handler, ebay_item=e_item)
                    if e_item:
                        if revise_inventory_only:
                            self.__do_revise_inventory(handler=handler, ebay_item=e_item)
                        else:
                            self.__do_revise(handler=handler, ebay_item=e_item)

                # make compatible with legacy ebay items (which matching by amazon asin, not parent_asin)
                ee_item = EbayItemModelManager.fetch_one(ebay_store_id=self.__ebay_store.id, asin=t.asin)
                if ee_item and ee_item.ebid not in self.__cached_ebids:
                    self.__cached_ebids[ee_item.ebid] = True
                    ee_item = self.__do_sync(handler=handler, ebay_item=ee_item)
                    if ee_item:
                        if revise_inventory_only:
                            self.__do_revise_inventory(handler=handler, ebay_item=ee_item)
                        else:
                            self.__do_revise(handler=handler, ebay_item=ee_item)

            if self.__maxed_out:
                logger.info("[{}] STOP LISTING - REACHED EBAY ITEM LIST LIMITATION".format(self.__ebay_store.username))
                break
        return True

    def close_spider(self, spider):
        if not isinstance(spider, AmazonAsinSpider) and not isinstance(spider, AmazonBaseSpider):
            return True
        if not hasattr(spider, 'task_id') or not spider.task_id:
            return True
        if not hasattr(spider, 'ebay_store_id') or not spider.ebay_store_id:
            return True
        if hasattr(spider, 'dont_list_ebay') and spider.dont_list_ebay:
            return True
        self.__ebay_store = EbayStoreModelManager.fetch_one(id=spider.ebay_store_id)
        if not self.__ebay_store:
            return False
        self.__task_id = spider.task_id
        self.__start_ebay_listing(list_new=spider.list_new,
            revise_inventory_only=spider.revise_inventory_only)
        return True

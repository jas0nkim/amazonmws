import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'scrapers', 'amzn'))

from amazonmws import settings as amazonmws_settings, utils as amazonmws_utils
from amazonmws.loggers import GrayLogger as logger
from amazonmws.model_managers import *
from amazonmws.errors import record_ebay_category_error

from atoe.actions import EbayItemAction


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
    __excl_brands = None

    def __init__(self, ebay_store, **kwargs):
        self.ebay_store = ebay_store
        if 'min_review_count' in kwargs:
            self.__min_review_count = kwargs['min_review_count']
        if 'asins_exclude' in kwargs:
            self.__asins_exclude = kwargs['asins_exclude']
        
        cmap = AtoECategoryMapModelManager.fetch()
        self.__atemap = { m.amazon_category:m.ebay_category_id for m in cmap }
        self.__excl_brands = ExclBrandModelManager.fetch()

    def __restock(self, amazon_item, ebay_item):
        succeed = False
        maxed_out = False

        action = EbayItemAction(ebay_store=self.ebay_store,
                    ebay_item=ebay_item)
        eb_price = amazonmws_utils.calculate_profitable_price(amazon_item.price, self.ebay_store)
        if eb_price <= 0:
            logger.error("[%s|ASIN:%s] No listing price available" % (self.ebay_store.username, amazon_item.asin))
            return (succeed, maxed_out)
        succeed = action.revise_item(eb_price, amazonmws_settings.EBAY_ITEM_DEFAULT_QUANTITY)
        maxed_out = action.maxed_out()
        if succeed:
            # store in database
            EbayItemModelManager.restock(ebay_item, eb_price, amazonmws_settings.EBAY_ITEM_DEFAULT_QUANTITY)
        return (succeed, maxed_out)

    def __list_new(self, amazon_item):
        succeed = False
        maxed_out = False

        action = EbayItemAction(ebay_store=self.ebay_store,
                    amazon_item=amazon_item)
        category_id = self.__atemap[amazon_item.category]

        eb_price = amazonmws_utils.calculate_profitable_price(amazon_item.price, self.ebay_store)
        if eb_price <= 0:
            logger.error("[%s|ASIN:%s] No listing price available" % (self.ebay_store.username, amazon_item.asin))
            return (succeed, maxed_out)

        picture_urls = action.upload_pictures(StormStore.find(AmazonItemPicture, 
            AmazonItemPicture.asin == amazon_item.asin))
        if len(picture_urls) < 1:
            logger.error("[%s|ASIN:%s] No item pictures available" % (self.ebay_store.username, amazon_item.asin))
            return (succeed, maxed_out)

        ebid = action.add_item(category_id, picture_urls, eb_price, amazonmws_settings.EBAY_ITEM_DEFAULT_QUANTITY)
        maxed_out = action.maxed_out()
        if ebid:
            # store in database
            EbayItemModelManager.create(self.ebay_store, amazon_item.asin, ebid, category_id, eb_price, amazonmws_settings.EBAY_ITEM_DEFAULT_QUANTITY)
            succeed = True
        return (succeed, maxed_out)

    def __aware_brand(self, amazon_item):
        if self.__excl_brands.count() < 1:
            return False
        for excl_brand in self.__excl_brands:
            if amazon_item.brand_name == excl_brand.brand_name:
                if not excl_brand.category: # brand should excluded from all categories
                    logger.warning('[ASIN:%s] reported brand - %s - ignoring...' % (amazon_item.asin, amazon_item.brand_name))
                    return True
                else:
                    if amazon_item.category.startswith(excl_brand.category):
                        logger.warning('[ASIN:%s] reported brand - %s - ignoring...' % (amazon_item.asin, amazon_item.brand_name))
                        return True
        return False

    def run(self):
        pref_cats = EbayStorePreferredCategoryModelManager.fetch(ebay_store=self.ebay_store)
        for pref_cat in pref_cats:
            count = 1
            items = AmazonItemModelManager.fetch_filtered(pref_cat, self.__min_review_count, asins_exclude=self.__asins_exclude)
            for amazon_item, ebay_item in items:
                if count > pref_cat.max_items:
                    break
                succeed, maxed_out = self.run_each(amazon_item, ebay_item)
                if succeed:
                    count += 1                
                if maxed_out:
                    logger.info("[%s] STOP LISTING - REACHED EBAY ITEM LIST LIMITATION" % self.ebay_store.username)
                    break
        return True

    def run_each(self, amazon_item, ebay_item=None):
        if self.__aware_brand(amazon_item):
            return (False, False)
        if amazon_item.category not in self.__atemap:
            logger.error("[%s] No category id found in map data - %s" % (self.ebay_store.username, amazon_item.category))
            record_ebay_category_error(
                '', 
                amazon_item.asin,
                amazon_item.category,
                None,
                '',
            )
            return (False, False)
        if not amazon_item.status:
            logger.error("[%s|ASIN:%s] amazon item is not available any more - no listing" % (self.ebay_store.username, amazon_item.asin))
            return (False, False)
        if not amazon_item.is_fba:
            logger.error("[%s|ASIN:%s] amazon item is not FBA - no listing" % (self.ebay_store.username, amazon_item.asin))
            return (False, False)
        if amazon_item.is_addon:
            logger.error("[%s|ASIN:%s] amazon item is add-on - no listing" % (self.ebay_store.username, amazon_item.asin))
            return (False, False)
        if ebay_item:
            return self.__restock(amazon_item, ebay_item)
        else:
            return self.__list_new(amazon_item)

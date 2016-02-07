import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'scrapers', 'amzn'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'rfi'))

import datetime
from django.utils import timezone

from amazonmws import settings as amazonmws_settings, utils as amazonmws_utils
from amazonmws.loggers import GrayLogger as logger, StaticFieldFilter, get_logger_name
from amazonmws.model_managers import *
from amazonmws.errors import record_ebay_category_error, GetOutOfLoop

from atoe.actions import EbayItemAction, EbayItemCategoryAction

from rfi_sources.models import AmazonItem


class ListingHandler(object):

    ebay_store = None
    # max_num_listing = None
    
    __min_review_count = None
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
        logger.addFilter(StaticFieldFilter(get_logger_name(), 'atoe_listing'))

    def __restock(self, amazon_item, ebay_item):
        succeed = False
        maxed_out = False

        action = EbayItemAction(ebay_store=self.ebay_store,
                    ebay_item=ebay_item)
        eb_price = amazonmws_utils.calculate_profitable_price(amazon_item.price, self.ebay_store)
        if eb_price <= 0:
            logger.error("[%s|ASIN:%s] No listing price available" % (self.ebay_store.username, amazon_item.asin))
            return (succeed, maxed_out)
        succeed = action.revise_inventory(eb_price, amazonmws_settings.EBAY_ITEM_DEFAULT_QUANTITY)
        maxed_out = action.maxed_out()
        if succeed:
            # store in database
            EbayItemModelManager.restock(ebay_item, eb_price, amazonmws_settings.EBAY_ITEM_DEFAULT_QUANTITY)
        return (succeed, maxed_out)

    def __list_new(self, amazon_item):
        succeed = False
        maxed_out = False

        if amazon_item.category in self.__atemap:
            category_id = self.__atemap[amazon_item.category]
        else:
            category_id = self.__find_ebay_category_id(amazon_item.title)
        
        if not category_id:
            logger.error("[%s] No category id found in map data - %s" % (self.ebay_store.username, amazon_item.category))
            record_ebay_category_error(
                '', 
                amazon_item.asin,
                amazon_item.category,
                None,
                '',
            )
            return (False, False)

        action = EbayItemAction(ebay_store=self.ebay_store,
                    amazon_item=amazon_item)
        eb_price = amazonmws_utils.calculate_profitable_price(amazon_item.price, self.ebay_store)
        if eb_price <= 0:
            logger.error("[%s|ASIN:%s] No listing price available" % (self.ebay_store.username, amazon_item.asin))
            return (succeed, maxed_out)

        picture_urls = action.upload_pictures(AmazonItemPictureModelManager.fetch(asin=amazon_item.asin))
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

    def __find_ebay_category_id(self, title):
        title = amazonmws_utils.to_keywords(title)
        if not title:
            return None
        ebay_action = EbayItemAction(ebay_store=self.ebay_store)
        return ebay_action.find_category_id(title)

    def __revise(self, ebay_item, pictures):
        action = EbayItemAction(ebay_store=self.ebay_store, ebay_item=ebay_item, amazon_item=ebay_item.amazon_item)

        picture_urls = []
        if pictures.count() > 0:
            picture_urls = action.upload_pictures(pictures)
            if len(picture_urls) < 1:
                logger.error("[%s|ASIN:%s] No item pictures available" % (self.ebay_store.username, ebay_item.amazon_item.asin))

        return action.revise_item(picture_urls=picture_urls)

    def run(self, order='rating', restockonly=False):
        """order: rating | discount, restockonly: boolean
        """
        if order == 'discount':
            items = AmazonItemModelManager.fetch_discount_for_listing(ebay_store=self.ebay_store)
            try:
                for amazon_item, ebay_item in items:
                    # in case having duplicated asin
                    if amazon_item.asin in self.__asins_exclude:
                        continue
                    succeed, maxed_out = self.run_each(amazon_item, ebay_item, restockonly)
                    if succeed:
                        self.__asins_exclude.append(amazon_item.asin)
                    if maxed_out:
                        raise GetOutOfLoop("[%s] STOP LISTING - REACHED EBAY ITEM LIST LIMITATION" % self.ebay_store.username)
            except GetOutOfLoop as e:
                logger.info(e)

        else: # rating
            pref_cats = EbayStorePreferredCategoryModelManager.fetch(ebay_store=self.ebay_store, status=1)
            try:
                for pref_cat in pref_cats:
                    items = AmazonItemModelManager.fetch_filtered_for_listing(pref_cat, 
                                self.__min_review_count, 
                                order=order,
                                asins_exclude=self.__asins_exclude,
                                listing_min_dollar=self.ebay_store.listing_min_dollar,
                                listing_max_dollar=self.ebay_store.listing_max_dollar)
                    for amazon_item, ebay_item in items:
                        count = 1
                        if count > pref_cat.max_items:
                            break
                        # in case having duplicated asin
                        if amazon_item.asin in self.__asins_exclude:
                            continue
                        succeed, maxed_out = self.run_each(amazon_item, ebay_item, restockonly)
                        if succeed:
                            self.__asins_exclude.append(amazon_item.asin)
                            count += 1
                        if maxed_out:
                            raise GetOutOfLoop("[%s] STOP LISTING - REACHED EBAY ITEM LIST LIMITATION" % self.ebay_store.username)
            except GetOutOfLoop as e:
                logger.info(e)
        return True

    def run_sold(self, order='most', restockonly=False, max_items=None):
        """order: most | recent, restockonly: boolean
        """
        try:
            count = 1
            items = AmazonItemModelManager.fetch_sold_for_listing(self.ebay_store, order)
            for amazon_item, ebay_item in items:
                if max_items and count > max_items:
                    raise GetOutOfLoop("[%s] STOP LISTING - REACHED SOLD ITEM LIST LIMITATION" % self.ebay_store.username)
                # in case having duplicated asin
                if amazon_item.asin in self.__asins_exclude:
                    continue
                succeed, maxed_out = self.run_each(amazon_item, ebay_item, restockonly)
                if succeed:
                    self.__asins_exclude.append(amazon_item.asin)
                    count += 1
                if maxed_out:
                    raise GetOutOfLoop("[%s] STOP LISTING - REACHED EBAY ITEM LIST LIMITATION" % self.ebay_store.username)
        except GetOutOfLoop as e:
            logger.info(e)
        return True

    def run_each(self, amazon_item, ebay_item=None, restockonly=False):
        if amazon_item.asin in self.__asins_exclude:
            return (False, False)
        if self.__aware_brand(amazon_item):
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
        if amazon_item.is_pantry:
            logger.error("[%s|ASIN:%s] amazon item is pantry - no listing" % (self.ebay_store.username, amazon_item.asin))
            return (False, False)
        if amazon_item.quantity < amazonmws_settings.AMAZON_MINIMUM_QUANTITY_FOR_LISTING:
            logger.error("[%s|ASIN:%s] amazon item available quantity is not enough - no listing" % (self.ebay_store.username, amazon_item.asin))
            return (False, False)
        if amazon_item.price < float(self.ebay_store.listing_min_dollar) if self.ebay_store.listing_min_dollar else 0.00:
            logger.error("[%s|ASIN:%s] amazon item's price is out of range - no listing" % (self.ebay_store.username, amazon_item.asin))
            return (False, False)
        if amazon_item.price > float(self.ebay_store.listing_max_dollar) if self.ebay_store.listing_max_dollar else 999999999.99:
            logger.error("[%s|ASIN:%s] amazon item's price is out of range - no listing" % (self.ebay_store.username, amazon_item.asin))
            return (False, False)
        if ebay_item:
            return self.__restock(amazon_item, ebay_item)
        else:
            if restockonly:
                logger.error("[%s|ASIN:%s] no new ebay listing allowed (restock only) - no listing" % (self.ebay_store.username, amazon_item.asin))
                return (False, False)
            else:
                return self.__list_new(amazon_item)

    def run_revise_pictures(self):
        ebay_items = EbayItemModelManager.fetch(ebay_store_id=self.ebay_store.id)
        for ebay_item in ebay_items:
            one_day_before = timezone.now() - datetime.timedelta(1) # updated within last 24 hours
            revised_pictures = AmazonItemPictureModelManager.fetch(asin=ebay_item.asin, created_at__gte=one_day_before)
            if revised_pictures.count() < 1:
                continue
            self.__revise(ebay_item, pictures=revised_pictures)
        return True


class CategoryHandler(object):

    def __init__(self, ebay_store, **kwargs):
        self.ebay_store = ebay_store
        logger.addFilter(StaticFieldFilter(get_logger_name(), 'atoe_category'))

    def store_full_categories(self):
        category_action = EbayItemCategoryAction(ebay_store=self.ebay_store)
        top_level_categories = category_action.get_top_level_categories()

        if len(top_level_categories) > 0:
            self._store_categories(categories=top_level_categories)

            for category in top_level_categories:
                sub_level_categories = category_action.get_categories(parent_category_id=category.get('CategoryID'), level_limit=1000)
                self._store_categories(categories=sub_level_categories)

    def _store_categories(self, categories):
        if len(categories) < 1:
            return False

        else:
            for category in categories:
                obj = EbayItemCategoryManager.save(
                    category_id=category.get('CategoryID'),
                    category_level=int(category.get('CategoryLevel')),
                    category_name=category.get('CategoryName'),
                    category_parent_id=category.get('CategoryParentID'),
                    auto_pay_enabled=True if category.get('AutoPayEnabled', 'false') == 'true' else False,
                    best_offer_enabled=True if category.get('BestOfferEnabled', 'false') == 'true' else False,
                    leaf_category=True if category.get('LeafCategory', 'false') == 'true' else False
                )

                # print obj
            return True

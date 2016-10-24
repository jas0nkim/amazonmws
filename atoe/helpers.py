import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'scrapers', 'amzn'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'rfi'))

import datetime
import json
from django.utils import timezone

from amazonmws import settings as amazonmws_settings, utils as amazonmws_utils
from amazonmws.loggers import GrayLogger as logger, StaticFieldFilter, get_logger_name
from amazonmws.model_managers import *
from amazonmws.errors import record_ebay_category_error, GetOutOfLoop

from atoe.actions import EbayItemAction, EbayItemCategoryAction, EbayOrderAction, EbayStoreCategoryAction
from atoe.utils import EbayItemVariationUtils

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

    __disallowed_category_keywords = [
        'knives',
        'knife',
        'blades',
        'blade',
    ]

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

    # not being used
    #
    # def __restock(self, amazon_item, ebay_item):
    #     succeed = False
    #     maxed_out = False

    #     action = EbayItemAction(ebay_store=self.ebay_store,
    #                 ebay_item=ebay_item)
    #     eb_price = amazonmws_utils.calculate_profitable_price(amazon_item.price, self.ebay_store)
    #     if eb_price <= 0:
    #         logger.error("[%s|ASIN:%s] No listing price available" % (self.ebay_store.username, amazon_item.asin))
    #         return (succeed, maxed_out)
    #     succeed = action.revise_inventory(eb_price=eb_price, 
    #         quantity=amazonmws_settings.EBAY_ITEM_DEFAULT_QUANTITY)
    #     maxed_out = action.maxed_out()
    #     if succeed:
    #         # store in database
    #         EbayItemModelManager.restock(ebay_item, eb_price, amazonmws_settings.EBAY_ITEM_DEFAULT_QUANTITY)
    #     return (succeed, maxed_out)

    def __list_new(self, amazon_item, ebay_category_id):
        succeed = False
        maxed_out = False

        if amazon_item.category and any(x in amazon_item.category.lower() for x in self.__disallowed_category_keywords):
            logger.error("[%s] Knives/Blades are not allowed to list - %s" % (self.ebay_store.username, amazon_item.category))
            return (False, False)

        if not ebay_category_id:
            logger.error("[%s] No category id found in map data - %s" % (self.ebay_store.username, amazon_item.category))
            record_ebay_category_error(
                '', 
                amazon_item.asin,
                amazon_item.category,
                None,
                '',
            )
            return (False, False)

        action = EbayItemAction(ebay_store=self.ebay_store, amazon_item=amazon_item)
        if amazon_item.price < 1:
            logger.error("[%s|ASIN:%s] No price found on this item" % (self.ebay_store.username, amazon_item.asin))
            return (succeed, maxed_out)
        
        eb_price = amazonmws_utils.calculate_profitable_price(amazon_item.price, self.ebay_store)
        picture_urls = action.upload_pictures(AmazonItemPictureModelManager.fetch(asin=amazon_item.asin))
        if len(picture_urls) < 1:
            logger.error("[%s|ASIN:%s] No item pictures available" % (self.ebay_store.username, amazon_item.asin))
            return (succeed, maxed_out)

        store_category_id, store_category_name = self.__find_ebay_store_category_info(amazon_category=amazon_item.category)

        ebid = action.add_item(category_id=ebay_category_id, 
                            picture_urls=picture_urls, 
                            eb_price=eb_price, 
                            quantity=amazonmws_settings.EBAY_ITEM_DEFAULT_QUANTITY,
                            description=EbayItemVariationUtils.build_item_description(amazon_item=amazon_item),
                            store_category_id=store_category_id)
        maxed_out = action.maxed_out()
        if ebid:
            # store in database
            obj, created = EbayItemModelManager.create(ebay_store=self.ebay_store, 
                                    asin=amazon_item.parent_asin, 
                                    ebid=ebid, 
                                    category_id=ebay_category_id, 
                                    eb_price=eb_price, 
                                    quantity=amazonmws_settings.EBAY_ITEM_DEFAULT_QUANTITY)
            if obj:
                succeed = True
        return (succeed, maxed_out)

    def __list_new_v(self, amazon_items, ebay_category_id):
        succeed = False
        maxed_out = False
        
        amazon_item = amazon_items.first()
        if amazon_item.category and any(x in amazon_item.category.lower() for x in self.__disallowed_category_keywords):
            logger.error("[%s] Knives/Blades are not allowed to list - %s" % (self.ebay_store.username, amazon_item.category))
            return (False, False)

        if not ebay_category_id:
            logger.error("[%s] No category id found in map data - %s" % (self.ebay_store.username, amazon_item.category))
            record_ebay_category_error(
                '', 
                amazon_item.asin,
                amazon_item.category,
                None,
                '',
            )
            return (False, False)

        action = EbayItemAction(ebay_store=self.ebay_store, amazon_item=amazon_item)
        is_shoe = EbayItemVariationUtils.is_shoe(category_id=ebay_category_id)
        common_pictures = EbayItemVariationUtils.get_variations_common_pictures(amazon_items=amazon_items)
        variations = EbayItemVariationUtils.build_variations_obj(ebay_store=self.ebay_store,
            amazon_items=amazon_items, 
            common_pictures=common_pictures, 
            is_shoe=is_shoe)
        store_category_id, store_category_name = self.__find_ebay_store_category_info(amazon_category=amazon_item.category)

        variations_item_specifics = EbayItemVariationUtils.build_item_specifics_for_multi_variations(
            amazon_item=amazon_items.first())
        if is_shoe:
            variations_item_specifics = EbayItemVariationUtils.build_item_specifics_for_shoe(
                amazon_item=amazon_items.first())
        # upload pictures to ebay server
        common_pictures = action.upload_pictures(common_pictures)
        ebid = action.add_item(category_id=ebay_category_id,
                        picture_urls=common_pictures, 
                        eb_price=None, 
                        quantity=None,
                        title=EbayItemVariationUtils.build_variations_common_title(amazon_items=amazon_items),
                        description=EbayItemVariationUtils.build_item_description(amazon_item=amazon_item),
                        store_category_id=store_category_id,
                        variations=variations,
                        variations_item_specifics=variations_item_specifics)
        maxed_out = action.maxed_out()
        if ebid:
            # store in database
            obj, created = EbayItemModelManager.create(ebay_store=self.ebay_store, 
                                    asin=amazon_item.parent_asin, 
                                    ebid=ebid, 
                                    category_id=ebay_category_id, 
                                    eb_price=variations['Variation'][0]['StartPrice'], # 1st variation's price
                                    quantity=None)
            if obj:
                for v in variations['Variation']:
                    a = AmazonItemModelManager.fetch_one(asin=v['SKU'])
                    if a is None:
                        continue
                    EbayItemVariationModelManager.create(ebay_item=obj,
                                                    ebid=ebid,
                                                    asin=v['SKU'],
                                                    specifics=a.variation_specifics,
                                                    eb_price=v['StartPrice'],
                                                    quantity=v['Quantity'])
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
                    if amazon_item.category and amazon_item.category.startswith(excl_brand.category):
                        logger.warning('[ASIN:%s] reported brand - %s - ignoring...' % (amazon_item.asin, amazon_item.brand_name))
                        return True
        return False

    def __find_ebay_category_id(self, amazon_item):
        if amazon_item.category in self.__atemap:
            return self.__atemap[amazon_item.category]
        else:
            keywords = amazonmws_utils.to_keywords(amazon_item.title)
            if not keywords:
                return None
            ebay_action = EbayItemAction(ebay_store=self.ebay_store)
            return ebay_action.find_category_id(keywords)

    def __find_ebay_store_category_info(self, amazon_category):
        try:
            root_category = [c.strip() for c in amazon_category.split(':')][0]
            ebay_store_category = EbayStoreCategoryModelManager.fetch_one(name=root_category)
            if ebay_store_category:
                return (ebay_store_category.category_id, root_category)
            else:
                action = EbayStoreCategoryAction(ebay_store=self.ebay_store)
                category_id = action.add(name=root_category)
                if not category_id:
                    return (None, None)
                result = EbayStoreCategoryModelManager.create(ebay_store=self.ebay_store, category_id=category_id, name=root_category)
                if not result:
                    return (None, None)
                return (category_id, root_category)
        except Exception as e:
            return (None, None)

    def __revise(self, ebay_item, amazon_item, pictures):
        action = EbayItemAction(ebay_store=self.ebay_store, ebay_item=ebay_item, amazon_item=amazon_item)

        picture_urls = []
        if pictures and pictures.count() > 0:
            picture_urls = action.upload_pictures(pictures)
            if len(picture_urls) < 1:
                if action.end_item():
                    EbayItemModelManager.inactive(ebay_item=ebay_item)
                logger.error("[%s|ASIN:%s] No item pictures available - inactive/end item" % (self.ebay_store.username, amazon_item.asin))
                return (False, False)
        store_category_id, store_category_name = self.__find_ebay_store_category_info(amazon_category=amazon_item.category)

        succeed = action.revise_item(picture_urls=picture_urls,
            description=EbayItemVariationUtils.build_item_description(amazon_item=amazon_item),
            store_category_id=store_category_id)
        return (succeed, False)

    def __revise_v(self, amazon_items, ebay_item):
        # multi-variation item only
        if not ebay_item:
            return (False, False)
        else:
            action = EbayItemAction(ebay_store=self.ebay_store, ebay_item=ebay_item, amazon_item=amazon_items.first())
            common_pictures = EbayItemVariationUtils.get_variations_common_pictures(amazon_items=amazon_items)
            store_category_id, store_category_name = self.__find_ebay_store_category_info(amazon_category=amazon_items.first().category)

            # compare amazon_items variations with existing(ebay_items) variations
            # 1. if there are new variation from amazon_items variations
            #   apply action.add_variations(ebay_item, variations)
            # 2. if there are deleting variations from ebay_items variations
            #   apply action.delete_variations(ebay_item, variations)
            # 3. modify all other variations
            #   apply action.modify_variations(ebay_item, variations)
            variation_comp_result = EbayItemVariationUtils.compare_item_variations(
                amazon_items=amazon_items, ebay_item=ebay_item)
            
            ebay_category_id = ebay_item.ebay_category_id
            if ebay_category_id is None:
                ebay_category_id = self.__find_ebay_category_id(amazon_item=amazon_items.first())
            
            is_shoe = EbayItemVariationUtils.is_shoe(category_id=ebay_category_id)

            if 'delete' in variation_comp_result and len(variation_comp_result['delete']) > 0:
                for deleting_asin in variation_comp_result['delete']:
                    if action.delete_variation(asin=deleting_asin):
                        # db update
                        EbayItemVariationModelManager.delete(ebid=ebay_item.ebid,
                            asin__in=[deleting_asin, ])
                    else:
                        # fallback to OOS
                        if action.revise_inventory(eb_price=None,
                            quantity=0,
                            asin=deleting_asin):
                            EbayItemVariationModelManager.oos(variation=EbayItemVariationModelManager.fetch_one(ebid=ebay_item.ebid, asin=deleting_asin))

            if 'add' in variation_comp_result and len(variation_comp_result['add']) > 0:
                adding_variations_obj = EbayItemVariationUtils.build_add_variations_obj(
                        ebay_store=self.ebay_store,
                        amazon_items=amazon_items,
                        excl_brands=self.__excl_brands,
                        common_pictures=common_pictures, 
                        adding_asins=variation_comp_result['add'],
                        is_shoe=is_shoe)
                if action.update_variations(variations=adding_variations_obj):
                    # db update
                    for v in adding_variations_obj['Variation']:
                        a = AmazonItemModelManager.fetch_one(asin=v['SKU'])
                        if a is None:
                            continue
                        variation_db_obj = EbayItemVariationModelManager.fetch_one(ebid=ebay_item.ebid,
                            asin=v['SKU'])
                        if not variation_db_obj:
                            EbayItemVariationModelManager.create(ebay_item=ebay_item,
                                                        ebid=ebay_item.ebid,
                                                        asin=v['SKU'],
                                                        specifics=a.variation_specifics,
                                                        eb_price=v['StartPrice'],
                                                        quantity=v['Quantity'])
                        else:
                            EbayItemVariationModelManager.update(variation=variation_db_obj,
                                                        specifics=a.variation_specifics,
                                                        eb_price=v['StartPrice'],
                                                        quantity=v['Quantity'])

            if 'modify' in variation_comp_result and len(variation_comp_result['modify']) > 0:
                # price/inventory update
                for m_asin in variation_comp_result['modify']:
                    for _a in amazon_items:
                        if _a.asin == m_asin:
                            eb_price = None
                            if _a.price > 1:
                                eb_price = amazonmws_utils.calculate_profitable_price(_a.price, self.ebay_store)
                            quantity = 0
                            if _a.is_listable(ebay_store=self.ebay_store,
                                excl_brands=self.__excl_brands):
                                quantity = amazonmws_settings.EBAY_ITEM_DEFAULT_QUANTITY
                            # revise multi-variation item
                            succeed = action.revise_inventory(eb_price=eb_price, quantity=quantity, asin=_a.asin)
                            if succeed:
                                # db update
                                var_obj = EbayItemVariationModelManager.fetch_one(ebid=ebay_item.ebid, 
                                    asin=_a.asin)
                                EbayItemVariationModelManager.update(variation=var_obj,
                                                            eb_price=eb_price,
                                                            quantity=quantity)
                            break


            # finally revise item content (title/description/pictures/store category id) itself only
            variations_item_specifics = EbayItemVariationUtils.build_item_specifics_for_multi_variations(
                amazon_item=amazon_items.first())
            if is_shoe:
                variations_item_specifics = EbayItemVariationUtils.build_item_specifics_for_shoe(
                    amazon_item=amazon_items.first())
            # upload pictures to ebay server
            common_pictures = action.upload_pictures(common_pictures)
            success = action.revise_item(title=EbayItemVariationUtils.build_variations_common_title(amazon_items=amazon_items),
                description=EbayItemVariationUtils.build_variations_common_description(amazon_items=amazon_items),
                picture_urls=common_pictures,
                store_category_id=store_category_id,
                variations_item_specifics=variations_item_specifics)
            return (success, False)

    def __oos_non_multi_variation(self, amazon_item, ebay_item):
        try:
            ebay_action = EbayItemAction(ebay_store=self.ebay_store, ebay_item=ebay_item, amazon_item=amazon_item)
            # revise non multi-variation item
            succeed = ebay_action.revise_inventory(eb_price=None, quantity=0)
            if succeed:
                EbayItemModelManager.oos(ebay_item)
            return (succeed, False)
        except Exception:
            return (False, False)

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

    def __is_variationable_category(self, category_id):
        if category_id is None:
            return False
        enabled = EbayCategoryFeaturesModelManager.variations_enabled(ebay_category_id=category_id)
        if enabled is not None:
            return enabled
        else:
            # find it with ebay api
            category_handler = CategoryHandler(ebay_store=self.ebay_store)
            category_features = category_handler.find_ebay_category_features(category_id=category_id)
            if category_features:
                ebay_category_name = None
                ate_maps = AtoECategoryMapModelManager.fetch(ebay_category_id=category_id)
                if ate_maps and ate_maps.count() > 0:
                    ebay_category_name = ate_maps.first().ebay_category_name
                EbayCategoryFeaturesModelManager.create(ebay_category_id=category_id,
                    ebay_category_name=ebay_category_name,
                    upc_enabled=category_features.get('UPCEnabled', False),
                    variations_enabled=category_features.get('VariationsEnabled', False)
                )
                return category_features.get('VariationsEnabled', False)
            else:
                return False

    def run_each(self, amazon_items, ebay_item=None, restockonly=False):
        if ebay_item and EbayItemModelManager.is_inactive(ebay_item): # inactive (ended) item. do nothing
            return (False, False)

        if not amazon_items:
            return (False, False)
        if amazon_items.__class__.__name__ == 'AmazonItem': # quirk: make compatible with old code
            amazon_items = AmazonItemModelManager.fetch_its_variations(parent_asin=amazon_items.parent_asin)
        # depends on number of amazon items given...
        if amazon_items.count() < 1:
            return (False, False)
        elif amazon_items.count() == 1:
            # no variation item
            amazon_item = amazon_items.first()
            if not amazon_item.is_listable(ebay_store=self.ebay_store, excl_brands=self.__excl_brands):
                if not ebay_item:
                    return (False, False)
                else:
                    return self.__oos_non_multi_variation(amazon_item=amazon_item, ebay_item=ebay_item)
            if ebay_item:
                return self.__revise(ebay_item=ebay_item,
                    amazon_item=amzon_item,
                    pictures=AmazonItemPictureModelManager.fetch(asin=amazon_item.asin))
            else:
                if restockonly:
                    logger.error("[%s|ASIN:%s] no new ebay listing allowed (restock only) - no listing" % (self.ebay_store.username, amazon_item.asin))
                    return (False, False)
                else:
                    suggested_ebay_category_id = self.__find_ebay_category_id(amazon_item=amazon_items.first())
                    return self.__list_new(amazon_item=amazon_item, ebay_category_id=suggested_ebay_category_id)
        else: # amazon_items.count() > 1
            # multi-variation item
            suggested_ebay_category_id = self.__find_ebay_category_id(amazon_item=amazon_items.first())
            if not self.__is_variationable_category(category_id=suggested_ebay_category_id):
                for a_item in amazon_items:
                    amazon_items = AmazonItemModelManager.fetch(asin=a_item.asin)
                    success, maxed_out = self.run_each(amazon_items=AmazonItemModelManager.fetch(asin=a_item.asin), 
                        ebay_item=ebay_item, 
                        restockonly=restockonly)
                    if maxed_out:
                        return (success, maxed_out)
                return (True, False)
            else:
                if ebay_item:
                    return self.__revise_v(amazon_items=amazon_items, ebay_item=ebay_item)
                else:
                    if restockonly:
                        logger.warning("[%s|ASIN:%s] no new ebay listing allowed (restock only) - no listing" % (self.ebay_store.username, amazon_items.first().asin))
                        return (False, False)
                    else:
                        return self.__list_new_v(amazon_items=amazon_items, ebay_category_id=suggested_ebay_category_id)
        return (False, False)

    # def run_revise_pictures(self):
    #     """ deprecated
    #     """
    #     ebay_items = EbayItemModelManager.fetch(ebay_store_id=self.ebay_store.id)
    #     for ebay_item in ebay_items:
    #         one_day_before = timezone.now(tz=amazonmws_utils.get_utc()) - datetime.timedelta(1) # updated within last 24 hours
    #         revised_pictures = AmazonItemPictureModelManager.fetch(asin=ebay_item.asin, created_at__gte=one_day_before)
    #         if revised_pictures.count() < 1:
    #             continue
    #         self.__revise(ebay_item, ebay_item.amazon_item, pictures=revised_pictures)
    #     return True

    def __legacy_revise_item(self, ebay_item):
        """ backward compatibility
        """
        amazon_item = AmazonItemModelManager.fetch_one(asin=ebay_item.asin)
        if not amazon_item:
            return (False, False)
        else:
            if not amazon_item.is_listable(ebay_store=self.ebay_store, excl_brands=self.__excl_brands):
                return self.__oos_non_multi_variation(amazon_item=amazon_item, ebay_item=ebay_item)
            return self.__revise(ebay_item=ebay_item,
                amazon_item=amzon_item,
                pictures=AmazonItemPictureModelManager.fetch(asin=amazon_item.asin))

    def revise_item(self, ebay_item):
        if not ebay_item:
            return (False, False)
        amazon_items = AmazonItemModelManager.fetch_its_variations(parent_asin=ebay_item.asin)
        if amazon_items.count() < 1:
            return self.__legacy_revise_item(ebay_item)
        elif amazon_items.count() == 1:
            # no variation item
            amazon_item = amazon_items.first()
            if not amazon_item.is_listable(ebay_store=self.ebay_store, excl_brands=self.__excl_brands):
                return self.__oos_non_multi_variation(amazon_item=amazon_item, ebay_item=ebay_item)
            return self.__revise(ebay_item=ebay_item,
                    amazon_item=amazon_item,
                    pictures=AmazonItemPictureModelManager.fetch(asin=amazon_item.asin))
        else: # amazon_items.count() > 1
            # multi-variation item
            return self.__revise_v(amazon_items=amazon_items, ebay_item=ebay_item)
        return (False, False)

    def revise_non_multivariation_item(self, ebay_item, amazon_item=None):
        if not amazon_item:
            amazon_item = ebay_item.amazon_item
        if not amazon_item: # still no amazon item found... return False
            logger.error("[EBID:{}] unable to find a related Amazon item".format(ebay_item.ebid))
            return False
        return self.__revise(ebay_item=ebay_item,
            amazon_item=amazon_item,
            pictures=AmazonItemPictureModelManager.fetch(asin=amazon_item.asin))

    def revise_item_title(self, ebay_item, amazon_item=None):
        if not amazon_item:
            amazon_item = ebay_item.amazon_item
        if not amazon_item: # still no amazon item found... return False
            logger.error("[EBID:{}] unable to find a related Amazon item".format(ebay_item.ebid))
            return False
        action = EbayItemAction(ebay_store=self.ebay_store, ebay_item=ebay_item, amazon_item=ebay_item.amazon_item)
        return action.revise_item_title()

    def revise_item_description(self, ebay_item, amazon_item=None):
        if not amazon_item:
            amazon_item = ebay_item.amazon_item
        if not amazon_item: # still no amazon item found... return False
            logger.error("[EBID:{}] unable to find a related Amazon item".format(ebay_item.ebid))
            return False
        action = EbayItemAction(ebay_store=self.ebay_store, ebay_item=ebay_item, amazon_item=ebay_item.amazon_item)
        return action.revise_item_description(
            description=EbayItemVariationUtils.build_item_description(amazon_item=ebay_item.amazon_item))

    def add_variations(self, ebay_item, adding_asins=[]):
        maxed_out = False
        if len(adding_asins) < 1:
            return (False, maxed_out)

        _ebay_item_variation_asins = EbayItemModelManager.fetch_variation_skus(ebay_item=ebay_item)
        for adding_asin in adding_asins:
            if adding_asin not in _ebay_item_variation_asins:
                _ebay_item_variation_asins.append(adding_asin)

        amazon_items = AmazonItemModelManager.fetch(asin__in=_ebay_item_variation_asins)
        action = EbayItemAction(ebay_store=self.ebay_store, ebay_item=ebay_item, amazon_item=amazon_items.first())
        adding_variations_obj = EbayItemVariationUtils.build_add_variations_obj(
                ebay_store=self.ebay_store,
                amazon_items=amazon_items,
                excl_brands=self.__excl_brands,
                common_pictures=EbayItemVariationUtils.get_variations_common_pictures(amazon_items=amazon_items),
                adding_asins=adding_asins,
                is_shoe=EbayItemVariationUtils.is_shoe(category_id=self.__find_ebay_category_id(amazon_item=amazon_items.first())))
        if action.update_variations(variations=adding_variations_obj):
            maxed_out = action.maxed_out()
            # db update
            for v in adding_variations_obj['Variation']:
                a = AmazonItemModelManager.fetch_one(asin=v['SKU'])
                if a is None:
                    continue
                variation_db_obj = EbayItemVariationModelManager.fetch_one(ebid=ebay_item.ebid,
                    asin=v['SKU'])
                if not variation_db_obj:
                    EbayItemVariationModelManager.create(ebay_item=ebay_item,
                                                ebid=ebay_item.ebid,
                                                asin=v['SKU'],
                                                specifics=a.variation_specifics,
                                                eb_price=v['StartPrice'],
                                                quantity=v['Quantity'])
                else:
                    EbayItemVariationModelManager.update(variation=variation_db_obj,
                                                specifics=a.variation_specifics,
                                                eb_price=v['StartPrice'],
                                                quantity=v['Quantity'])
            return (True, maxed_out)
        return (False, maxed_out)

    def revise_variations(self, ebay_item, revising_asins=[]):
        maxed_out = False
        if len(revising_asins) < 1:
            return (False, maxed_out)

        _amazon_items = AmazonItemModelManager.fetch(asin__in=revising_asins)
        if _amazon_items.count() < 1:
            return (False, maxed_out)

        action = EbayItemAction(ebay_store=self.ebay_store, ebay_item=ebay_item, amazon_item=_amazon_items.first())
        for _a in _amazon_items:
            if not _a or not _a.status:
                # delete
                if action.delete_variation(asin=_a.asin):
                    # db update
                    EbayItemVariationModelManager.delete(ebid=ebay_item.ebid,
                        asin__in=[_a.asin, ])
                else:
                    # fallback to OOS
                    if action.revise_inventory(eb_price=None,
                        quantity=0,
                        asin=_a.asin):
                        EbayItemVariationModelManager.oos(variation=EbayItemVariationModelManager.fetch_one(ebid=ebay_item.ebid, asin=_a.asin))
            else:
                # modify
                eb_price = None
                if _a.price > 1:
                    eb_price = amazonmws_utils.calculate_profitable_price(_a.price, self.ebay_store)
                quantity = 0
                if _a.is_listable(ebay_store=self.ebay_store,
                    excl_brands=self.__excl_brands):
                    quantity = amazonmws_settings.EBAY_ITEM_DEFAULT_QUANTITY
                # revise multi-variation item
                if action.revise_inventory(eb_price=eb_price, quantity=quantity, asin=_a.asin)
                    # db update
                    EbayItemVariationModelManager.update(
                            variation=EbayItemVariationModelManager.fetch_one(ebid=ebay_item.ebid, asin=_a.asin),
                            eb_price=eb_price,
                            quantity=quantity)
        return (True, maxed_out)


class CategoryHandler(object):

    def __init__(self, ebay_store, **kwargs):
        self.ebay_store = ebay_store
        logger.addFilter(StaticFieldFilter(get_logger_name(), 'atoe_category'))

    def find_ebay_category(self, string):
        keywords = amazonmws_utils.to_keywords(string)
        if not keywords:
            return (None, None)

        ebay_action = EbayItemAction(ebay_store=self.ebay_store)
        ebay_category_info = ebay_action.find_category(keywords)
        if not ebay_category_info:
            return (None, None)
        return ebay_category_info

    def find_ebay_category_features(self, category_id):
        ebay_action = EbayItemAction(ebay_store=self.ebay_store)
        try:
            return ebay_action.get_category_features(category_id=category_id)
        except Exception as e:
            logger.exception("Failed to find ebay category features - {}".format(str(e)))
            return None

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


class OrderShippingTrackingHandler(object):

    ebay_store = None
    amazon_account = None

    def __init__(self, ebay_store, amazon_account=None):
        self.ebay_store = ebay_store
        self.amazon_account = amazon_account
        logger.addFilter(StaticFieldFilter(get_logger_name(), 'order_shipping_tracking'))

    def set_shipping_tracking_information(self, ebay_order_id, carrier, tracking_number):
        ebay_order = EbayOrderModelManager.fetch_one(order_id=ebay_order_id)
        if not ebay_order:
            return False

        action = EbayOrderAction(ebay_store=self.ebay_store)
        result = action.set_shipping_tracking_info(ebay_order=ebay_order, 
            carrier=carrier, tracking_number=tracking_number)

        if not result:
            logger.info('[{}] failed to send tracking information to ebay - [ {} : {} ]'.format(ebay_order_id, carrier, tracking_number))
            return False
        else:
            # create new ebay_order_shippings entry
            ebay_order_shipping = EbayOrderShippingModelManager.create(order_id=ebay_order_id,
                carrier=carrier, tracking_number=tracking_number)
            if not ebay_order_shipping:
                return False

            # append tracking info into associated amazon_order entry, if possible
            ordered_pair = EbayOrderAmazonOrderModelManager.fetch_one(ebay_order_id=ebay_order_id)
            if ordered_pair and ordered_pair.amazon_order:
                AmazonOrderModelManager.update(amazon_order=ordered_pair.amazon_order,
                    carrier=carrier, tracking_number=tracking_number)

            return ebay_order_shipping


class FeedbackLeavingHandler(object):

    ebay_store = None
    amazon_account = None

    def __init__(self, ebay_store, amazon_account=None):
        self.ebay_store = ebay_store
        self.amazon_account = amazon_account
        logger.addFilter(StaticFieldFilter(get_logger_name(), 'feedback_leaving'))

    def leave_feedback(self, ebay_order):
        action = EbayOrderAction(ebay_store=self.ebay_store)
        result = action.leave_feedback(ebay_order=ebay_order)

        if not result:
            logger.info('[{}] failed leave a feedback'.format(ebay_order.order_id))
            return False
        else:
            # update ebay_order entry
            updating = EbayOrderModelManager.update(order=ebay_order, feedback_left=True)
            if not updating:
                return False
            ebay_item = EbayOrderItemModelManager.fetch(order_id=ebay_order.order_id)[:1].get()
            # send thank you message to buyer
            action.send_message_to_buyer(ebay_order=ebay_order,
                ebid=ebay_item.ebid,
                question_type="Shipping",
                subject=self.ebay_store.message_on_shipping_subject,
                body=self.ebay_store.message_on_shipping_body
            )
            return True

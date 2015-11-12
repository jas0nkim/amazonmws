import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

import datetime

from storm.expr import Select, And, Desc
from storm.exceptions import StormError

from amazonmws import settings
from amazonmws.models import StormStore, EbayStore, EbayItem, zzAmazonItem as AmazonItem, zzAmazonItemPicture as AmazonItemPicture, zzAtoECategoryMap as AtoECategoryMap, zzAmazonItemOffer as AmazonItemOffer, zzAmazonBestsellers as AmazonBestsellers,zzEbayStorePreferredCategory as EbayStorePreferredCategory
from amazonmws.loggers import GrayLogger as logger


class AmazonItemModelManager(object):

    @staticmethod
    def fetch_one(asin):
        try:
            ret = StormStore.find(AmazonItem, AmazonItem.asin == asin).one()
        except StormError, e:
            ret = None
        return ret

    @staticmethod
    def fetch_filtered(preferred_category, min_review_count, **kw):
        """filter amazon item by given a preferred category of a ebay store:
            - amazon active items
            - FBA items
            - not add-on items
            - item which has not listed at ebay store
            return type: list
        """
        result = []
        filtered_items = []
        try:
            if preferred_category.category_type == 'amazon':
                filtered_items = StormStore.find(AmazonItem,
                    AmazonItem.category.startswith(preferred_category.category_name),
                    AmazonItem.status == AmazonItem.STATUS_ACTIVE,
                    AmazonItem.is_fba == True,
                    AmazonItem.is_addon == False,
                    AmazonItem.quantity >= settings.AMAZON_MINIMUM_QUANTITY_FOR_LISTING,
                    AmazonItem.review_count >= min_review_count
                ).order_by(Desc(AmazonItem.avg_rating), 
                    Desc(AmazonItem.review_count))
            else: # amazon_bestseller
                filtered_items = StormStore.find(AmazonItem,
                    AmazonItem.asin == AmazonBestsellers.asin,
                    AmazonBestsellers.bestseller_category == preferred_category.category_name,
                    AmazonItem.status == AmazonItem.STATUS_ACTIVE,
                    AmazonItem.is_fba == True,
                    AmazonItem.is_addon == False,
                    AmazonItem.quantity >= settings.AMAZON_MINIMUM_QUANTITY_FOR_LISTING,
                    AmazonItem.review_count >= min_review_count
                ).order_by(AmazonBestsellers.rank)

        except StormError:
            logger.exception('Unable to filter amazon items')

        # workaround solution - stupid but storm doesn't support outer join...
        # what it supposes to do - i.e.
        #   SELECT * FROM pets AS p 
        #       LEFT OUTER JOIN lost-pets AS lp
        #       ON p.name = lp.name
        #       WHERE lp.id IS NULL
        #       
        # ref: http://stackoverflow.com/a/369861
        num_items = 0

        for amazon_item in filtered_items:
            # asins_exclude
            asins_exclude = []
            if 'asins_exclude' in kw:
                asins_exclude = kw['asins_exclude']
            if  isinstance(asins_exclude, list) and len(asins_exclude) > 0:
                if amazon_item.asin in asins_exclude:
                    continue
            
            # ebay_item
            ebay_item = None
            try:
                ebay_item = StormStore.find(EbayItem, 
                    EbayItem.ebay_store_id == preferred_category.ebay_store_id,
                    EbayItem.asin == amazon_item.asin).one()
            except StormError, e:
                logger.exception(e)
                continue

            if not ebay_item:
                num_items += 1
                item_set = (amazon_item, None)
                result.append(item_set)
            elif ebay_item.status == EbayItem.STATUS_OUT_OF_STOCK:
                """add OOS ebay item - need to restock to ebay because it's been restocked on amazon!
                """
                num_items += 1
                item_set = (amazon_item, ebay_item)
                result.append(item_set)

        logger.info("[ebay store id:%s] Number of items to list on ebay: %d items" % (preferred_category.ebay_store_id, num_items))
        return result


class AtoECategoryMapModelManager(object):

    @staticmethod
    def fetch():
        return StormStore.find(AtoECategoryMap)

    @staticmethod
    def fetch_one(amazon_category):
        try:
            ret = StormStore.find(AtoECategoryMap, 
                AtoECategoryMap.amazon_category == amazon_category).one()
        except StormError, e:
            logger.exception(e)
            ret = None
        return ret

    @staticmethod
    def create(amazon_category, **kw):
        try:
            cmap = AtoECategoryMap()
            cmap.amazon_category = amazon_category
            if 'ebay_category_id' in kw and kw['ebay_category_id'] != None:
                cmap.ebay_category_id = unicode(kw['ebay_category_id'])
            if 'ebay_category_name' in kw and kw['ebay_category_name'] != None:
                cmap.ebay_category_name = unicode(kw['ebay_category_name'])
            cmap.created_at = datetime.datetime.now()
            cmap.updated_at = datetime.datetime.now()
            StormStore.add(cmap)
            StormStore.commit()
            return True
        except StormError, e:
            StormStore.rollback()
            logger.exception("[AtoECategoryMapModelManager] Failed to store information on create new amazon to ebay category map - amazon category - %s" % amazon_category)
            return False
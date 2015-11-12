import datetime

from storm.expr import Select, And, Desc
from storm.exceptions import StormError

from . import settings
from .models import StormStore, EbayStore, EbayItem, zzAmazonItem as AmazonItem, zzAmazonItemPicture as AmazonItemPicture, zzAtoECategoryMap as AtoECategoryMap, zzAmazonItemOffer as AmazonItemOffer, zzAmazonBestsellers as AmazonBestsellers,zzEbayStorePreferredCategory as EbayStorePreferredCategory
from .loggers import GrayLogger as logger


class EbayStoreModelManager(object):

    @staticmethod
    def fetch():
        return StormStore.find(EbayStore)

    @staticmethod
    def fetch_one(ebay_store_id):
        try:
            return StormStore.find(EbayStore, EbayStore.ebay_store_id == ebay_store_id).one()
        except StormError:
            logger.exception("[ebay store id:%s] Failed to fetch an ebay store" % ebay_store_id)
            return None


class EbayStorePreferredCategoryModelManager(object):

    @staticmethod
    def fetch(ebay_store):
        return StormStore.find(EbayStorePreferredCategory, 
                EbayStorePreferredCategory.ebay_store_id == ebay_store.id
            ).order_by(EbayStorePreferredCategory.priority)


class EbayItemModelManager(object):

    @staticmethod
    def create(ebay_store, asin, ebid, category_id, eb_price, quantity):
        try:
            ebay_item = EbayItem()
            ebay_item.ebay_store_id = ebay_store.id
            ebay_item.asin = asin
            ebay_item.ebid = ebid
            ebay_item.ebay_category_id = category_id
            ebay_item.eb_price = eb_price
            ebay_item.quantity = quantity
            ebay_item.status = EbayItem.STATUS_ACTIVE
            ebay_item.created_at = datetime.datetime.now()
            ebay_item.updated_at = datetime.datetime.now()
            StormStore.add(ebay_item)
            StormStore.commit()
            return True
        except StormError:
            StormStore.rollback()
            logger.exception("[%s|ASIN:%s|EBID:%s] Failed to store information on create new item" % (ebay_store.username, asin, ebid))
            return False

    @staticmethod
    def update_price(ebay_item, eb_price):
        try:
            ebay_item.eb_price = eb_price
            ebay_item.updated_at = datetime.datetime.now()
            StormStore.add(ebay_item)
            StormStore.commit()
            return True
        except StormError:
            StormStore.rollback()
            logger.exception("[ASIN:%s|EBID:%s] Failed to store information on update item price" % (ebay_item.asin, ebay_item.ebid))
            return False

    @staticmethod
    def restock(ebay_item, eb_price, quantity):
        try:
            ebay_item.eb_price = eb_price
            ebay_item.quantity = quantity
            ebay_item.status = EbayItem.STATUS_ACTIVE
            ebay_item.updated_at = datetime.datetime.now()
            StormStore.add(ebay_item)
            StormStore.commit()
            return True
        except StormError:
            StormStore.rollback()
            logger.exception("[ASIN:%s|EBID:%s] Failed to store information on restock item" % (ebay_item.asin, ebay_item.ebid))
            return False

    @staticmethod
    def oos(ebay_item):
        try:
            ebay_item.quantity = 0
            ebay_item.status = EbayItem.STATUS_OUT_OF_STOCK
            ebay_item.updated_at = datetime.datetime.now()
            StormStore.add(ebay_item)
            StormStore.commit()
            return True
        except StormError:
            StormStore.rollback()
            logger.exception("[ASIN:%s|EBID:%s] Failed to store information on oos item" % (ebay_item.asin, ebay_item.ebid))
            return False

    @staticmethod
    def inactive(ebay_item):
        try:
            ebay_item.status = EbayItem.STATUS_INACTIVE
            ebay_item.updated_at = datetime.datetime.now()
            StormStore.add(ebay_item)
            StormStore.commit()
            return True
        except StormError:
            StormStore.rollback()
            logger.exception("[ASIN:%s|EBID:%s] Failed to store information on end item" % (ebay_item.asin, ebay_item.ebid))
            return False

    @staticmethod
    def fetch(**kw):
        expressions = []
        if 'asin' in kw:
            expressions += [ EbayItem.asin == kw['asin'] ]
        if 'ebay_store_id' in kw:
            expressions += [ EbayItem.ebay_store_id == kw['ebay_store_id'] ]
        
        return StormStore.find(EbayItem, And(*expressions))

    @staticmethod
    def fetch_distinct_asin():
        subselect = Select(EbayItem.asin, distinct=True)
        return StormStore.find(EbayItem, EbayItem.asin.is_in(subselect))

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

import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

import datetime

from storm.expr import Select, And, Desc
from storm.exceptions import StormError

from amazonmws import settings
from amazonmws.models import StormStore, EbayStore, EbayItem, zzAmazonItem as AmazonItem, zzAmazonItemPicture as AmazonItemPicture, zzAtoECategoryMap as AtoECategoryMap, zzAmazonItemOffer as AmazonItemOffer, zzAmazonBestsellers as AmazonBestsellers,zzEbayStorePreferredCategory as EbayStorePreferredCategory
from amazonmws.loggers import GrayLogger as logger


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
    def reduce_quantity(ebay_item, reduce_by=1):
        if ebay_item.quantity < 1:
            logger.error("[ASIN:%s|EBID:%s] Unable to reduce quantity - already less than 1" % (ebay_item.asin, ebay_item.ebid))
            return False
        try:
            ebay_item.quantity -= reduce_by
            if ebay_item.quantity < 1:
                ebay_item.status = EbayItem.STATUS_OUT_OF_STOCK
            ebay_item.updated_at = datetime.datetime.now()
            StormStore.add(ebay_item)
            StormStore.commit()
            return True
        except StormError:
            StormStore.rollback()
            logger.exception("[ASIN:%s|EBID:%s] Failed to store information on update item quantity" % (ebay_item.asin, ebay_item.ebid))
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
    def inactive(**kw):
        ebay_item = None
        if 'ebay_item' in kw:
            ebay_item = kw['ebay_item']
        elif 'ebid' in kw:
            ebay_item = EbayItemModelManager.fetch_one(ebid=kw['ebid'])

        if not ebay_item:
            return False
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
    def fetch(order=None, desc=False, **kw):
        expressions = []
        if 'asin' in kw:
            expressions += [ EbayItem.asin == kw['asin'] ]
        if 'ebay_store_id' in kw:
            expressions += [ EbayItem.ebay_store_id == kw['ebay_store_id'] ]        
        if 'status' in kw:
            expressions += [ EbayItem.status == kw['status'] ]
        if len(expressions) > 0:
            ebay_items = StormStore.find(EbayItem, And(*expressions))
        else:
            ebay_items = StormStore.find(EbayItem)
        if order:
            if desc == True:
                ebay_items.order_by(Desc(getattr(EbayItem, order)))
            else:
                ebay_items.order_by(getattr(EbayItem, order))
        return ebay_items

    @staticmethod
    def fetch_one(**kw):
        try:
            if 'ebid' in kw:
                return StormStore.find(EbayItem, EbayItem.ebid == kw['ebid']).one()
            elif 'ebay_store_id' in kw and 'asin' in kw:
                return StormStore.find(EbayItem, 
                            EbayItem.ebay_store_id == kw['ebay_store_id'],
                            EbayItem.asin == kw['asin']).one()
            else:
                return None
        except StormError:
            logger.exception("[EBID:%s] Failed to fetch an ebay item" % ebid)
            return None

    @staticmethod
    def fetch_distinct_asin():
        subselect = Select(EbayItem.asin, distinct=True)
        return StormStore.find(EbayItem, EbayItem.asin.is_in(subselect))

    @staticmethod
    def is_active(ebay_item):
        if ebay_item.status == EbayItem.STATUS_ACTIVE:
            return True
        return False

    @staticmethod
    def is_inactive(ebay_item):
        if ebay_item.status == EbayItem.STATUS_INACTIVE:
            return True
        return False

    @staticmethod
    def is_oos(ebay_item):
        if ebay_item.status == EbayItem.STATUS_OUT_OF_STOCK:
            return True
        return False

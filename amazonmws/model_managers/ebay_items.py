import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'rfi'))

from django.core.exceptions import MultipleObjectsReturned

from amazonmws import settings
from amazonmws.loggers import GrayLogger as logger

from rfi_listings.models import EbayItem


class EbayItemModelManager(object):

    @staticmethod
    def create(ebay_store, asin, ebid, category_id, eb_price, quantity):
        kw = {
            'ebay_store_id': ebay_store.id,
            'asin': asin,
            'ebid': ebid,
            'ebay_category_id': category_id,
            'eb_price': eb_price,
            'quantity': quantity,
            'status': EbayItem.STATUS_ACTIVE,
        }
        obj, created = EbayItem.objects.update_or_create(**kw)
        return created

    @staticmethod
    def update_price_and_active(ebay_item, eb_price):
        return EbayItemModelManager.restock(ebay_item=ebay_item, eb_price=eb_price, quantity=settings.EBAY_ITEM_DEFAULT_QUANTITY)

    @staticmethod
    def reduce_quantity(ebay_item, reduce_by=1):
        if isinstance(ebay_item, EbayItem):
            if ebay_item.quantity < 1:
                logger.error("[ASIN:%s|EBID:%s] Unable to reduce quantity - already less than 1" % (ebay_item.asin, ebay_item.ebid))
                return False

            ebay_item.quantity -= reduce_by
            if ebay_item.quantity < 1:
                ebay_item.status = EbayItem.STATUS_OUT_OF_STOCK
            ebay_item.save()
            return True
        return False

    @staticmethod
    def restock(ebay_item, eb_price, quantity):
        if isinstance(ebay_item, EbayItem):
            ebay_item.eb_price = eb_price
            ebay_item.quantity = quantity
            ebay_item.status = EbayItem.STATUS_ACTIVE
            ebay_item.save()
            return True
        return False

    @staticmethod
    def oos(ebay_item):
        if isinstance(ebay_item, EbayItem):
            ebay_item.quantity = 0
            ebay_item.status = EbayItem.STATUS_OUT_OF_STOCK
            ebay_item.save()
            return True
        return False

    @staticmethod
    def inactive(**kw):
        ebay_item = None
        if 'ebay_item' in kw:
            ebay_item = kw['ebay_item']
        elif 'ebid' in kw:
            try:
                ebay_item = EbayItem.objects.get(ebid=kw['ebid'])
            except MultipleObjectsReturned as e:
                logger.error("[EBID:%s] Multile ebay items exist" % kw['ebid'])
                return False
            except EbayItem.DoesNotExist as e:
                logger.warning("[EBID:%s] No ebay item found" % kw['ebid'])
                return False

        if isinstance(ebay_item, EbayItem):
            ebay_item.quantity = 0
            ebay_item.status = EbayItem.STATUS_INACTIVE
            ebay_item.save()
            return True
        return False

    @staticmethod
    def fetch(order=None, desc=False, **kw):
        ebay_items = EbayItem.objects.filter(**kw)
        if order:
            if desc == True:
                ebay_items.order_by('-{}'.format(order))
            else:
                ebay_items.order_by(order)
        return ebay_items

    @staticmethod
    def fetch_one(**kw):
        if 'ebid' in kw:
            try:
                return EbayItem.objects.get(ebid=kw['ebid'])
            except MultipleObjectsReturned as e:
                logger.error("[EBID:%s] Multile ebay items exist" % kw['ebid'])
                return None
            except EbayItem.DoesNotExist as e:
                logger.warning("[EBID:%s] No ebay item found" % kw['ebid'])
                return None

        elif 'ebay_store_id' in kw and 'asin' in kw:
            try:
                return EbayItem.objects.get(
                    ebay_store_id=kw['ebay_store_id'],
                    asin=kw['asin']
                )
            except MultipleObjectsReturned as e:
                logger.error("[EbayStoreID:%d|ASIN:%s] Multile ebay items exist" % (kw['ebay_store_id'], kw['asin']))
                return None
            except EbayItem.DoesNotExist as e:
                logger.warning("[EbayStoreID:%d|ASIN:%s] No ebay item found" % (kw['ebay_store_id'], kw['asin']))
                return None

        else:
            return None

    @staticmethod
    def fetch_distinct_asin(**kw):
        return EbayItem.objects.filter(**kw).values_list('asin', flat=True).distinct()

    @staticmethod
    def is_active(ebay_item):
        if isinstance(ebay_item, EbayItem) and ebay_item.status == EbayItem.STATUS_ACTIVE:
            return True
        return False

    @staticmethod
    def is_inactive(ebay_item):
        if isinstance(ebay_item, EbayItem) and ebay_item.status == EbayItem.STATUS_INACTIVE:
            return True
        return False

    @staticmethod
    def is_oos(ebay_item):
        if isinstance(ebay_item, EbayItem) and ebay_item.status == EbayItem.STATUS_OUT_OF_STOCK:
            return True
        return False

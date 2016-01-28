import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'rfi'))

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

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
    def update_price(ebay_item, eb_price):
        if isinstance(ebay_item, EbayItem):
            ebay_item.update(eb_price=eb_price)
            return True
        return False

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
            ebay_item.update(
                eb_price=eb_price, 
                quantity=quantity,
                status=EbayItem.STATUS_ACTIVE
            )
            return True
        return False

    @staticmethod
    def oos(ebay_item):
        if isinstance(ebay_item, EbayItem):
            ebay_item.update(
                quantity=0,
                status=EbayItem.STATUS_OUT_OF_STOCK
            )
            return True
        return False

    @staticmethod
    def inactive(**kw):
        ebay_item = None
        if 'ebay_item' in kw:
            ebay_item = kw['ebay_item']
        elif 'ebid' in kw:
            ebay_item = EbayItem.objects.get(ebid=kw['ebid'])

        if isinstance(ebay_item, EbayItem):
            ebay_item.update(status=EbayItem.STATUS_INACTIVE)
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
        try:
            if 'ebid' in kw:
                return EbayItem.objects.get(ebid=kw['ebid'])
            elif 'ebay_store_id' in kw and 'asin' in kw:
                return EbayItem.objects.get(
                    ebay_store_id=kw['ebay_store_id'],
                    asin=kw['asin']
                )
            else:
                return None
        except MultipleObjectsReturned as e:
            logger.exception("[EBID:%s] Multile ebay items exist" % ebid)
            return None
        except ObjectDoesNotExist as e:
            logger.exception("[EBID:%s] Failed to fetch an ebay item" % ebid)
            return None

    @staticmethod
    def fetch_distinct_asin():
        return EbayItem.objects.distinct('asin')

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

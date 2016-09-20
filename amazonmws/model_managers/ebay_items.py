import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'rfi'))

from django.core.exceptions import MultipleObjectsReturned

from amazonmws import settings
from amazonmws.loggers import GrayLogger as logger

from rfi_listings.models import EbayItem, EbayItemVariation, EbayItemStat, EbayCategoryFeatures, EbayStoreCategory


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
        return EbayItem.objects.update_or_create(**kw) # (obj, created)

    @staticmethod
    def update_category(ebay_item, ebay_category_id):
        if isinstance(ebay_item, EbayItem):
            ebay_item.ebay_category_id = ebay_category_id
            ebay_item.save()
            return True
        return False

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
                ebay_items = ebay_items.order_by('-{}'.format(order))
            else:
                ebay_items = ebay_items.order_by(order)
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

    @staticmethod
    def fetch_variations(ebay_item):
        variations = EbayItemVariationModelManager.fetch(ebid=ebay_item.ebid)
        if not variations or variations.count() < 1:
            return None
        else:
            return variations

    @staticmethod
    def fetch_variation_skus(ebay_item):
        variations = EbayItemModelManager.fetch_variations(ebay_item)
        if not variations:
            return []
        else:
            return [ v.asin for v in variations ]


class EbayItemVariationModelManager(object):

    @staticmethod
    def create(ebay_item, ebid, asin, specifics, eb_price, quantity):
        kw = {
            'ebay_item_id': ebay_item.id,
            'ebid': ebid,
            'asin': asin,
            'specifics': specifics,
            'eb_price': eb_price,
            'quantity': quantity,
        }
        obj, created = EbayItemVariation.objects.update_or_create(**kw)
        return created

    @staticmethod
    def fetch(**kw):
        return EbayItemVariation.objects.filter(**kw)

    @staticmethod
    def fetch_one(**kw):
        if 'ebid' in kw and 'asin' in kw:
            try:
                return EbayItemVariation.objects.get(
                    ebid=kw['ebid'],
                    asin=kw['asin'])
            except MultipleObjectsReturned as e:
                logger.error("[EBID:%d|ASIN:%s] Multile ebay item variations exist" % (kw['ebid'], kw['asin']))
                return None
            except EbayItemVariation.DoesNotExist as e:
                logger.warning("[EBID:%d|ASIN:%s] No ebay item variation found" % (kw['ebid'], kw['asin']))
                return None
        else:
            return None

    @staticmethod
    def update(variation, **kw):
        if isinstance(variation, EbayItemVariation):
            for key, value in kw.iteritems():
                setattr(variation, key, value)
            variation.save()
            return True
        return False

    @staticmethod
    def delete(**kw):
        if 'ebid' in kw and 'asin__in' in kw:
            AmazonItemPicture.objects.filter(**kw).delete()
            return True
        return False


class EbayItemStatModelManager(object):

    @staticmethod
    def create(ebid, clicks, watches, solds):
        kw = {
            'ebid': ebid,
            'clicks': clicks,
            'watches': watches,
            'solds': solds,
        }
        obj, created = EbayItemStat.objects.update_or_create(**kw)
        return created

    @staticmethod
    def fetch(**kw):
        return EbayItemStat.objects.filter(**kw)


class EbayCategoryFeaturesModelManager(object):
    @staticmethod
    def create(ebay_category_id, ebay_category_name=None, upc_enabled=None, variations_enabled=False):
        kw = {
            'ebay_category_id': ebay_category_id,
            'ebay_category_name': ebay_category_name,
            'upc_enabled': upc_enabled,
            'variations_enabled': variations_enabled,
        }
        obj, created = EbayCategoryFeatures.objects.update_or_create(**kw)
        return created

    @staticmethod
    def fetch(**kw):
        return EbayCategoryFeatures.objects.filter(**kw)

    @staticmethod
    def fetch_one(**kw):
        if 'ebay_category_id' in kw:
            try:
                return EbayCategoryFeatures.objects.get(ebay_category_id=kw['ebay_category_id'])
            except MultipleObjectsReturned as e:
                logger.error("[CategoryID:%s] Multile ebay category features exist" % kw['ebay_category_id'])
                return None
            except EbayCategoryFeatures.DoesNotExist as e:
                logger.warning("[CategoryID:%s] No ebay category feature found" % kw['ebay_category_id'])
                return None
        elif 'id' in kw:
            try:
                return EbayCategoryFeatures.objects.get(id=kw['id'])
            except MultipleObjectsReturned as e:
                logger.error("[CategoryName:%s] Multile ebay category features exist" % kw['id'])
                return None
            except EbayCategoryFeatures.DoesNotExist as e:
                logger.warning("[CategoryName:%s] No ebay category feature found" % kw['id'])
                return None
        else:
            return None

    @staticmethod
    def variations_enabled(**kw):
        if 'ebay_category_id' in kw:
            features = EbayCategoryFeaturesModelManager.fetch_one(ebay_category_id=kw['ebay_category_id'])
            if features:
                return features.variations_enabled
            else:
                return False
        else:
            return False


class EbayStoreCategoryModelManager(object):

    @staticmethod
    def create(ebay_store, category_id, name, parent_category_id=-999, order=0):
        kw = {
            'ebay_store_id': ebay_store.id,
            'category_id': category_id,
            'parent_category_id': parent_category_id,
            'name': name,
            'order': order,
        }
        obj, created = EbayStoreCategory.objects.update_or_create(**kw)
        return created

    @staticmethod
    def fetch_one(**kw):
        if 'category_id' in kw:
            try:
                return EbayStoreCategory.objects.get(category_id=kw['category_id'])
            except MultipleObjectsReturned as e:
                logger.error("[CategoryID:%s] Multile ebay store categories exist" % kw['category_id'])
                return None
            except EbayStoreCategory.DoesNotExist as e:
                logger.warning("[CategoryID:%s] No ebay store category found" % kw['category_id'])
                return None
        elif 'name' in kw:
            try:
                return EbayStoreCategory.objects.get(name=kw['name'])
            except MultipleObjectsReturned as e:
                logger.error("[CategoryName:%s] Multile ebay store categories exist" % kw['name'])
                return None
            except EbayStoreCategory.DoesNotExist as e:
                logger.warning("[CategoryName:%s] No ebay store category found" % kw['name'])
                return None
        else:
            return None

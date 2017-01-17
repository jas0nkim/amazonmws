import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'rfi'))

from django.core.exceptions import MultipleObjectsReturned

from amazonmws import settings
from amazonmws.loggers import GrayLogger as logger

from rfi_sources.models import *


class AliexpressItemModelManager(object):

    @staticmethod
    def create(**kw):
        obj = None
        try:
            obj = AliexpressItem(**kw)
            obj.save()
        except Exception as e:
            logger.error(str(e))
            return None
        return obj

    @staticmethod
    def update(item, **kw):
        if isinstance(item, AliexpressItem):
            for key, value in kw.iteritems():
                setattr(item, key, value)
            item.save()
            return True
        return False

    @staticmethod
    def delete(**kw):
        if 'alxid' in kw:
            AliexpressItem.objects.filter(**kw).delete()
            return True
        return False

    @staticmethod
    def fetch(**kw):
        return AliexpressItem.objects.filter(**kw)

    @staticmethod
    def fetch_one(**kw):
        if 'alxid' in kw:
            try:
                return AliexpressItem.objects.get(alxid=kw['alxid'])
            except MultipleObjectsReturned as e:
                logger.error("[ALXID:{}] Multile aliexpress items exist".format(kw['alxid']))
                return None
            except AliexpressItem.DoesNotExist as e:
                logger.warning("[ALXID:{}] No aliexpress item found".format(kw['alxid']))
                return None
        else:
            return None

    @staticmethod
    def inactive(item):
        return AliexpressItemModelManager.update(item, status=0)


class AliexpressItemDescriptionModelManager(object):

    @staticmethod
    def create(**kw):
        obj = None
        try:
            obj = AliexpressItemDescription(**kw)
            obj.save()
        except Exception as e:
            logger.error(str(e))
            return None
        return obj

    @staticmethod
    def update(item_description, **kw):
        if isinstance(item_description, AliexpressItemDescription):
            for key, value in kw.iteritems():
                setattr(item_description, key, value)
            item_description.save()
            return True
        return False

    @staticmethod
    def delete(**kw):
        if 'alxid' in kw:
            AliexpressItemDescription.objects.filter(**kw).delete()
            return True
        return False

    @staticmethod
    def fetch(**kw):
        return AliexpressItemDescription.objects.filter(**kw)

    @staticmethod
    def fetch_one(**kw):
        if 'alxid' in kw:
            try:
                return AliexpressItemDescription.objects.get(alxid=kw['alxid'])
            except MultipleObjectsReturned as e:
                logger.error("[ALXID:{}] Multile aliexpress item descriptions exist".format(kw['alxid']))
                return None
            except AliexpressItemDescription.DoesNotExist as e:
                logger.warning("[ALXID:{}] No aliexpress item description found".format(kw['alxid']))
                return None
        else:
            return None


class AliexpressItemSkuModelManager(object):

    @staticmethod
    def create(**kw):
        obj = None
        try:
            obj = AliexpressItemSku(**kw)
            obj.save()
        except Exception as e:
            logger.error(str(e))
            return None
        return obj

    @staticmethod
    def update(item_sku, **kw):
        if isinstance(item_sku, AliexpressItemSku):
            for key, value in kw.iteritems():
                setattr(item_sku, key, value)
            item_sku.save()
            return True
        return False

    @staticmethod
    def delete(**kw):
        if 'alxid' in kw:
            AliexpressItemSku.objects.filter(**kw).delete()
            return True
        return False

    @staticmethod
    def fetch(**kw):
        return AliexpressItemSku.objects.filter(**kw)

    @staticmethod
    def fetch_one(**kw):
        if 'alxid' in kw:
            try:
                return AliexpressItemSku.objects.get(alxid=kw['alxid'])
            except MultipleObjectsReturned as e:
                logger.error("[ALXID:{}] Multile aliexpress item sku exist".format(kw['alxid']))
                return None
            except AliexpressItemSku.DoesNotExist as e:
                logger.warning("[ALXID:{}] No aliexpress item sku found".format(kw['alxid']))
                return None
        else:
            return None


class AliexpressItemShippingModelManager(object):

    @staticmethod
    def create(**kw):
        obj = None
        try:
            obj = AliexpressItemShipping(**kw)
            obj.save()
        except Exception as e:
            logger.error(str(e))
            return None
        return obj

    @staticmethod
    def update(item_shipping, **kw):
        if isinstance(item_shipping, AliexpressItemShipping):
            for key, value in kw.iteritems():
                setattr(item_shipping, key, value)
            item_shipping.save()
            return True
        return False

    @staticmethod
    def delete(**kw):
        if 'alxid' in kw:
            AliexpressItemShipping.objects.filter(**kw).delete()
            return True
        return False

    @staticmethod
    def fetch(**kw):
        return AliexpressItemShipping.objects.filter(**kw)

    @staticmethod
    def fetch_one(**kw):
        if 'alxid' in kw:
            try:
                return AliexpressItemShipping.objects.get(alxid=kw['alxid'])
            except MultipleObjectsReturned as e:
                logger.error("[ALXID:{}] Multile aliexpress item shipping exist".format(kw['alxid']))
                return None
            except AliexpressItemShipping.DoesNotExist as e:
                logger.warning("[ALXID:{}] No aliexpress item shipping found".format(kw['alxid']))
                return None
        else:
            return None


class AliexpressItemApparelModelManager(object):

    @staticmethod
    def create(**kw):
        obj = None
        try:
            obj = AliexpressItemApparel(**kw)
            obj.save()
        except Exception as e:
            logger.error(str(e))
            return None
        return obj

    @staticmethod
    def update(item_apparel, **kw):
        if isinstance(item_apparel, AliexpressItemApparel):
            for key, value in kw.iteritems():
                setattr(item_apparel, key, value)
            item_apparel.save()
            return True
        return False

    @staticmethod
    def delete(**kw):
        if 'alxid' in kw:
            AliexpressItemApparel.objects.filter(**kw).delete()
            return True
        return False

    @staticmethod
    def fetch(**kw):
        return AliexpressItemApparel.objects.filter(**kw)

    @staticmethod
    def fetch_one(**kw):
        if 'alxid' in kw:
            try:
                return AliexpressItemApparel.objects.get(alxid=kw['alxid'])
            except MultipleObjectsReturned as e:
                logger.error("[ALXID:{}] Multile aliexpress item apparels exist".format(kw['alxid']))
                return None
            except AliexpressItemApparel.DoesNotExist as e:
                logger.warning("[ALXID:{}] No aliexpress item apparel found".format(kw['alxid']))
                return None
        else:
            return None


class AliexpressCategoryModelManager(object):

    @staticmethod
    def create(**kw):
        obj = None
        try:
            obj = AliexpressCategory(**kw)
            obj.save()
        except Exception as e:
            logger.error(str(e))
            return None
        return obj

    @staticmethod
    def update(category, **kw):
        if isinstance(category, AliexpressCategory):
            for key, value in kw.iteritems():
                setattr(category, key, value)
            category.save()
            return True
        return False

    @staticmethod
    def delete(**kw):
        if 'category_id' in kw:
            AliexpressCategory.objects.filter(**kw).delete()
            return True
        return False

    @staticmethod
    def fetch(**kw):
        return AliexpressCategory.objects.filter(**kw)

    @staticmethod
    def fetch_one(**kw):
        if 'category_id' in kw:
            try:
                return AliexpressCategory.objects.get(category_id=kw['category_id'])
            except MultipleObjectsReturned as e:
                logger.error("[ALXCATID:{}] Multile aliexpress categories exist".format(kw['category_id']))
                return None
            except AliexpressCategory.DoesNotExist as e:
                logger.warning("[ALXCATID:{}] No aliexpress category found".format(kw['category_id']))
                return None
        else:
            return None


class AlxToEbayCategoryMapModelManager(object):

    @staticmethod
    def create(**kw):
        obj = None
        try:
            obj = AlxToEbayCategoryMap(**kw)
            obj.save()
        except Exception as e:
            logger.error(str(e))
            return None
        return obj

    @staticmethod
    def update(c_map, **kw):
        if isinstance(c_map, AlxToEbayCategoryMap):
            for key, value in kw.iteritems():
                setattr(c_map, key, value)
            c_map.save()
            return True
        return False

    @staticmethod
    def delete(**kw):
        if 'aliexpress_category' in kw:
            AlxToEbayCategoryMap.objects.filter(**kw).delete()
            return True
        return False

    @staticmethod
    def fetch(**kw):
        return AlxToEbayCategoryMap.objects.filter(**kw)

    @staticmethod
    def fetch_one(**kw):
        if 'aliexpress_category' in kw:
            try:
                return AlxToEbayCategoryMap.objects.get(aliexpress_category=kw['aliexpress_category'])
            except MultipleObjectsReturned as e:
                logger.error("[ALXCAT:{}] Multile aliexpress-ebay category map exist".format(kw['aliexpress_category']))
                return None
            except AlxToEbayCategoryMap.DoesNotExist as e:
                logger.warning("[ALXCAT:{}] No aliexpress-ebay category map found".format(kw['aliexpress_category']))
                return None
        else:
            return None

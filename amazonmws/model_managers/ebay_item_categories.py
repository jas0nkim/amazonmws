import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'rfi'))

from django.core.exceptions import MultipleObjectsReturned

from amazonmws import settings
from amazonmws.loggers import GrayLogger as logger

from rfi_sources.models import EbayItemCategory


class EbayItemCategoryManager(object):

    @staticmethod
    def create(**kw):
        try:
            obj = EbayItemCategory(**kw)
            obj.save()
        except Exception as e:
            logger.error(str(e))
            return None
        return obj

    @staticmethod
    def update(category, **kw):
        if isinstance(category, EbayItemCategory):
            for key, value in kw.iteritems():
                setattr(category, key, value)
            category.save()
            return category
        return None

    @staticmethod
    def fetch_one(**kw):
        if 'category_id' in kw:
            try:
                return EbayItemCategory.objects.get(category_id=kw['category_id'])
            except MultipleObjectsReturned as e:
                logger.error("[EBCATID:{}] Multile ebay categories exist".format(kw['category_id']))
                return None
            except EbayItemCategory.DoesNotExist as e:
                logger.warning("[EBCATID:{}] - DoesNotExist: EbayItemCategory matching query does not exist. Create one!".format(kw['category_id']))
                return None
        else:
            return None

    @staticmethod
    def save(**kw):
        if 'category_id' in kw:
            category = EbayItemCategoryManager.fetch_one(category_id=kw['category_id'])
            if category:
                return EbayItemCategoryManager.update(category, **kw)
            else:
                return EbayItemCategoryManager.create(**kw)
        else:
            obj, created = EbayItemCategory.objects.update_or_create(**kw)
        return obj

    @staticmethod
    def get_top_category(category_or_category_id):
        category = None
        if isinstance(category_or_category_id, EbayItemCategory):
            category = category_or_category_id
        else:
            category = EbayItemCategoryManager.fetch_one(category_id=category_or_category_id)

        if not category:
            return None
        if category.category_level == 1:
            return category
        else:
            return EbayItemCategoryManager.get_top_category(
                category_or_category_id=EbayItemCategoryManager.get_parent_category(category))

    @staticmethod
    def get_second_top_category(category_or_category_id):
        category = None
        if isinstance(category_or_category_id, EbayItemCategory):
            category = category_or_category_id
        else:
            category = EbayItemCategoryManager.fetch_one(category_id=category_or_category_id)

        if not category:
            return None
        if category.category_level == 1 or category.category_level == 2:
            return category
        else:
            return EbayItemCategoryManager.get_second_top_category(
                category_or_category_id=EbayItemCategoryManager.get_parent_category(category))

    @staticmethod
    def get_parent_category(category_or_category_id):
        category = None
        if isinstance(category_or_category_id, EbayItemCategory):
            category = category_or_category_id
        else:
            category = EbayItemCategoryManager.fetch_one(category_id=category_or_category_id)

        if not category:
            return None
        if category.category_level == 1:
            return category
        else:
            return EbayItemCategoryManager.fetch_one(category_id=category.category_parent_id)

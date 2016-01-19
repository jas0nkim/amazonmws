import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'rfi'))

import datetime

# from storm.expr import Select, And, Desc, Not, SQLRaw
# from storm.exceptions import StormError

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from amazonmws import settings
# from amazonmws.models import StormStore, EbayStore, EbayItem, Transaction, zzAmazonItem as AmazonItem, zzAmazonItemPicture as AmazonItemPicture, zzAtoECategoryMap as AtoECategoryMap, zzAmazonItemOffer as AmazonItemOffer, zzAmazonBestsellers as AmazonBestsellers,zzEbayStorePreferredCategory as EbayStorePreferredCategory, zzExclBrand as ExclBrand

from rfi_sources.models import AmazonItem, AmazonItemPicture, AmazonItemOffer, AToECategoryMap, AmazonBestseller

from amazonmws.loggers import GrayLogger as logger


class AmazonItemModelManager(object):

    @staticmethod
    def create(**kw):
        obj, created = AmazonItem.objects.update_or_create(**kw)
        return created

    @staticmethod
    def update(item, **kw):
        if isinstance(item, AmazonItem):
            item.update(**kw)
            return True
        return False

    @staticmethod
    def inactive(item):
        return AmazonItemModelManager.update(item, status=AmazonItem.STATUS_INACTIVE)        

    @staticmethod
    def fetch(**kw):
        # make compatible with django query
        if 'category_startswith' in kw:
            kw['category__startswith'] = kw['category_startswith']
            del kw['category_startswith']
        
        return AmazonItem.objects.filter(**kw)

    @staticmethod
    def fetch_one(asin):
        try:
            return AmazonItem.objects.get(asin=asin)
        except MultipleObjectsReturned as e:
            logger.error("[ASIN:%s] Multiple amazon item exists in the system" % asin)
            return None
        except ObjectDoesNotExist as e:
            logger.error("[ASIN:%s] Amazon item does not exist in the system" % asin)
            return None

    @staticmethod
    def _fetch_for_listing(results, ebay_store):
        pass

    @staticmethod
    def fetch_sold_for_listing(ebay_store, order='most'):
        pass

    @staticmethod
    def fetch_discount_for_listing(ebay_store):
        pass

    @staticmethod
    def fetch_filtered_for_listing(preferred_category, min_review_count, **kw):
        pass


class AmazonItemPictureModelManager(object):

    @staticmethod
    def create(**kw):
        pass

    @staticmethod
    def fetch_one(asin, picture_url):
        pass


class AmazonBestsellersModelManager(object):

    @staticmethod
    def create(**kw):
        pass

    @staticmethod
    def update(bestseller, **kw):
        pass
    
    @staticmethod
    def fetch_one(bestseller_category_url, rank):
        pass

    @staticmethod
    def fetch(**kw):
        pass


class AmazonItemOfferModelManager(object):

    @staticmethod
    def create(**kw):
        pass

    @staticmethod
    def update(offer, **kw):
        pass

    @staticmethod
    def fetch_one(asin, is_fba, merchant_id, merchant_name):
        pass


class AtoECategoryMapModelManager(object):

    @staticmethod
    def fetch(**kw):
        pass

    @staticmethod
    def fetch_one(amazon_category):
        pass

    @staticmethod
    def create(amazon_category, **kw):
        pass

    @staticmethod
    def update(cmap, **kw):
        pass


class ExclBrandModelManager(object):

    @staticmethod
    def fetch():
        pass        

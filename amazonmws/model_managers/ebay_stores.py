import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

import datetime

from storm.expr import Select, And, Desc
from storm.exceptions import StormError

from amazonmws import settings
from amazonmws.models import StormStore, EbayStore, EbayItem, zzAmazonItem as AmazonItem, zzAmazonItemPicture as AmazonItemPicture, zzAtoECategoryMap as AtoECategoryMap, zzAmazonItemOffer as AmazonItemOffer, zzAmazonBestsellers as AmazonBestsellers,zzEbayStorePreferredCategory as EbayStorePreferredCategory
from amazonmws.loggers import GrayLogger as logger


class EbayStoreModelManager(object):

    @staticmethod
    def fetch():
        return StormStore.find(EbayStore)

    @staticmethod
    def fetch_one(**kw):
        try:
            if 'ebay_store_id' in kw:
                return StormStore.find(EbayStore, EbayStore.ebay_store_id == kw['ebay_store_id']).one()
            elif 'username' in kw:
                return StormStore.find(EbayStore, EbayStore.username == kw['username']).one()
            else:
                return None
        except StormError:
            logger.exception("Failed to fetch an ebay store")
            return None


class EbayStorePreferredCategoryModelManager(object):

    @staticmethod
    def fetch(ebay_store):
        return StormStore.find(EbayStorePreferredCategory, 
                EbayStorePreferredCategory.ebay_store_id == ebay_store.id
            ).order_by(EbayStorePreferredCategory.priority)

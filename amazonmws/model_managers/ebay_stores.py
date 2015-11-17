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
            if 'id' in kw:
                return StormStore.find(EbayStore, EbayStore.id == kw['id']).one()
            elif 'username' in kw:
                return StormStore.find(EbayStore, EbayStore.username == kw['username']).one()
            else:
                return None
        except StormError:
            logger.exception("Failed to fetch an ebay store")
            return None


class EbayStorePreferredCategoryModelManager(object):

    @staticmethod
    def fetch(**kw):
        expressions = []
        expressions += [ EbayStorePreferredCategory.status == EbayStorePreferredCategory.STATUS_ACTIVE ]
        if 'ebay_store' in kw:
            ebay_store = kw['ebay_store']
            expressions += [ EbayStorePreferredCategory.ebay_store_id == ebay_store.id ]
        return StormStore.find(EbayStorePreferredCategory, And(*expressions)).order_by(EbayStorePreferredCategory.priority)

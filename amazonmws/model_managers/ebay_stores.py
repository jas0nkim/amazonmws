import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'rfi'))

import random

from django.core.exceptions import MultipleObjectsReturned

from amazonmws import settings
from amazonmws.loggers import GrayLogger as logger

from rfi_account_profiles.models import EbayStore
from rfi_listings.models import EbayStorePreferredCategory


class EbayStoreModelManager(object):

    @staticmethod
    def fetch():
        return EbayStore.objects.all()

    @staticmethod
    def fetch_one(**kw):
        if 'id' in kw:
            try:
                return EbayStore.objects.get(id=kw['id'])
            except MultipleObjectsReturned as e:
                logger.error("[EbayStoreID:%s] Multiple ebay store exists in the system" % kw['id'])
                return None
            except EbayStore.DoesNotExist as e:
                logger.error("[EbayStoreID:%s] Ebay store does not exist in the system" % kw['id'])
                return None

        elif 'username' in kw:
            try:
                return EbayStore.objects.get(username=kw['username'])
            except MultipleObjectsReturned as e:
                logger.error("[EbayUsername:%s] Multiple ebay store exists in the system" % kw['username'])
                return None
            except EbayStore.DoesNotExist as e:
                logger.error("[EbayUsername:%s] Ebay store does not exist in the system" % kw['username'])
                return None
    
        elif 'random' in kw and kw['random'] == True:
            _store_ids = []
            _all_stores = EbayStoreModelManager.fetch()
            for _store in _all_stores:
                _store_ids.append(_store.id)
            if len(_store_ids) > 0:
                return EbayStoreModelManager.fetch_one(id=random.choice(_store_ids))
            else:
                return None
        else:
            return None


class EbayStorePreferredCategoryModelManager(object):

    @staticmethod
    def fetch(**kw):
        # make compatible with django query
        if 'ebay_store' in kw and isinstance(kw['ebay_store'], EbayStore):
            kw['ebay_store_id'] = kw['ebay_store'].id
            del kw['ebay_store']

        return EbayStorePreferredCategory.objects.filter(**kw).order_by('priority')

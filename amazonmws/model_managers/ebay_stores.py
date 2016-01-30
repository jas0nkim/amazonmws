import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'rfi'))

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

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
        try:
            if 'id' in kw:
                return EbayStore.objects.get(id=kw['id'])
            elif 'username' in kw:
                return EbayStore.objects.get(username=kw['username'])
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
        except MultipleObjectsReturned as e:
            logger.error("[ASIN:%s] Multiple amazon item exists in the system" % asin)
            return None
        except ObjectDoesNotExist as e:
            logger.error("[ASIN:%s] Amazon item does not exist in the system" % asin)
            return None


class EbayStorePreferredCategoryModelManager(object):

    @staticmethod
    def fetch(**kw):
        # make compatible with django query
        if 'ebay_store' in kw and isinstance(kw['ebay_store'], EbayStore)::
            kw['ebay_store_id'] = kw['ebay_store'].id
            del kw['ebay_store']

        return EbayStorePreferredCategory.objects.filter(**kw).order_by('priority')

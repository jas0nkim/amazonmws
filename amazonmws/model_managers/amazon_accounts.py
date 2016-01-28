import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'rfi'))

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from amazonmws import settings
from amazonmws.loggers import GrayLogger as logger

from rfi_account_profiles.models import AmazonAccount


class AmazonAccountModelManager(object):

    @staticmethod
    def fetch():
        return AmazonAccount.objects.all()

    @staticmethod
    def fetch_one(**kw):
        try:
            if 'id' in kw:
                return AmazonAccount.objects.get(id=kw['id'])
            elif 'email' in kw:
                return AmazonAccount.objects.get(email=kw['email'])
            elif 'ebay_store_id' in kw:
                return AmazonAccount.objects.get(ebay_stores__id=kw['ebay_store_id'])
            else:
                return None
        except MultipleObjectsReturned as e:
            logger.exception("More than one amazon account found")
            return None
        except DoesNotExist as e:
            logger.exception("Failed to fetch an amazon account")
            return None

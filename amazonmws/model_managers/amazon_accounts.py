import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'rfi'))

from django.core.exceptions import MultipleObjectsReturned

from amazonmws import settings
from amazonmws.loggers import GrayLogger as logger

from rfi_account_profiles.models import AmazonAccount


class AmazonAccountModelManager(object):

    @staticmethod
    def fetch():
        return AmazonAccount.objects.all()

    @staticmethod
    def fetch_one(**kw):
        if 'id' in kw:
            try:
                return AmazonAccount.objects.get(id=kw['id'])
            except MultipleObjectsReturned as e:
                logger.error("[AmazonAccountID:%d] More than one amazon account found" % kw['id'])
                return None
            except AmazonAccount.DoesNotExist as e:
                logger.warning("[AmazonAccountID:%d] No amazon account found. Create one!" % kw['id'])
                return None

        elif 'email' in kw:
            try:
                return AmazonAccount.objects.get(email=kw['email'])
            except MultipleObjectsReturned as e:
                logger.error("[AmazonEmail:%s] More than one amazon account found" % kw['email'])
                return None
            except AmazonAccount.DoesNotExist as e:
                logger.warning("[AmazonEmail:%s] No amazon account found. Create one!" % kw['email'])
                return None

        elif 'ebay_store_id' in kw:
            try:
                return AmazonAccount.objects.get(ebay_stores__id=kw['ebay_store_id'])
            except MultipleObjectsReturned as e:
                logger.error("[EbayStoreID:%d] More than one amazon account found" % kw['ebay_store_id'])
                return None
            except AmazonAccount.DoesNotExist as e:
                logger.warning("[EbayStoreID:%d] No amazon account found. Create one!" % kw['ebay_store_id'])
                return None

        else:
            return None

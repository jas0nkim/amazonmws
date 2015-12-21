import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

import datetime

from storm.expr import Select, And, Desc
from storm.exceptions import StormError

from amazonmws import settings
from amazonmws.models import StormStore, EbayStore, AmazonAccount, EbayStoreAmazonAccount
from amazonmws.loggers import GrayLogger as logger


class AmazonAccountModelManager(object):

    @staticmethod
    def fetch():
        return StormStore.find(AmazonAccount)

    @staticmethod
    def fetch_one(**kw):
        try:
            if 'id' in kw:
                return StormStore.find(AmazonAccount, AmazonAccount.id == kw['id']).one()
            elif 'email' in kw:
                return StormStore.find(AmazonAccount, AmazonAccount.email == kw['email']).one()
            elif 'ebay_store_id' in kw:
                expressions = []
                expressions += [ AmazonAccount.id == EbayStoreAmazonAccount.amazon_account_id ]
                expressions += [ EbayStoreAmazonAccount.ebay_store_id == kw['ebay_store_id'] ]
                return StormStore.find(AmazonAccount, And(*expressions)).one()
            else:
                return None
        except StormError:
            logger.exception("Failed to fetch an amazon account")
            return None

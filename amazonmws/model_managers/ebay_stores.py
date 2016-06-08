import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'rfi'))

import random

from django.core.exceptions import MultipleObjectsReturned

from amazonmws import settings
from amazonmws.loggers import GrayLogger as logger

from rfi_account_profiles.models import EbayStore
from rfi_listings.models import EbayStorePreferredCategory, AmazonScrapeTask


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
                logger.warning("[EbayStoreID:%s] Ebay store does not exist in the system" % kw['id'])
                return None

        elif 'username' in kw:
            try:
                return EbayStore.objects.get(username=kw['username'])
            except MultipleObjectsReturned as e:
                logger.error("[EbayUsername:%s] Multiple ebay store exists in the system" % kw['username'])
                return None
            except EbayStore.DoesNotExist as e:
                logger.warning("[EbayUsername:%s] Ebay store does not exist in the system" % kw['username'])
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
        return EbayStorePreferredCategory.objects.filter(**kw).order_by('priority')


class AmazonScrapeTaskModelManager(object):

    @staticmethod
    def fetch(**kw):
        return AmazonScrapeTask.objects.filter(**kw)

    @staticmethod
    def fetch_one(**kw):
        if 'id' in kw:
            try:
                return AmazonScrapeTask.objects.get(id=kw['id'])
            except MultipleObjectsReturned as e:
                logger.error("[AmazonScrapeTaskID:%s] Multiple Amazon Scrape Task exists in the system" % kw['id'])
                return None
            except AmazonScrapeTask.DoesNotExist as e:
                logger.warning("[AmazonScrapeTaskID:%s] Amazon Scrape Task does not exist in the system" % kw['id'])
                return None

        elif 'task_id' in kw and 'ebay_store_id' in kw and 'asin' in kw:
            try:
                return AmazonScrapeTask.objects.get(task_id=kw['task_id'], ebay_store_id=kw['ebay_store_id'], asin=kw['asin'])
            except MultipleObjectsReturned as e:
                logger.error("[TaskID:%s, ASIN:%s] Multiple Amazon Scrape Task exists in the system" % (kw['task_id'], kw['asin']))
                return None
            except AmazonScrapeTask.DoesNotExist as e:
                logger.warning("[TaskID:%s, ASIN:%s] Amazon Scrape Task does not exist in the system" % (kw['task_id'], kw['asin']))
                return None
        else:
            return None

    @staticmethod
    def create(**kw):
        obj, created = AmazonScrapeTask.objects.update_or_create(**kw)
        return created

import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'rfi'))

from django.core.exceptions import MultipleObjectsReturned

from amazonmws import settings
from amazonmws.loggers import GrayLogger as logger

from rfi_sources.models import *


class AliexpressStoreModelManager(object):

    @staticmethod
    def create(**kw):
        obj = None
        try:
            obj = AliexpressStore(**kw)
            obj.save()
        except Exception as e:
            logger.error(str(e))
            return None
        return obj

    @staticmethod
    def update(store, **kw):
        if isinstance(store, AliexpressStore):
            for key, value in kw.iteritems():
                setattr(store, key, value)
            store.save()
            return True
        return False

    @staticmethod
    def delete(**kw):
        if 'store_id' in kw:
            AliexpressStore.objects.filter(**kw).delete()
            return True
        return False

    @staticmethod
    def fetch(**kw):
        return AliexpressStore.objects.filter(**kw)

    @staticmethod
    def fetch_one(**kw):
        if 'store_id' in kw:
            try:
                return AliexpressStore.objects.get(store_id=kw['store_id'])
            except MultipleObjectsReturned as e:
                logger.error("[ALXSTOREID:{}] Multile aliexpress stores exist".format(kw['store_id']))
                return None
            except AliexpressStore.DoesNotExist as e:
                logger.warning("[ALXSTOREID:{}] No aliexpress store found".format(kw['store_id']))
                return None
        else:
            return None

    @staticmethod
    def inactive(item):
        return AliexpressStoreModelManager.update(item, status=0)


class AliexpressStoreFeedbackModelManager(object):

    @staticmethod
    def create(**kw):
        obj = None
        try:
            obj = AliexpressStoreFeedback(**kw)
            obj.save()
        except Exception as e:
            logger.error(str(e))
            return None
        return obj

    @staticmethod
    def update(store_feedback, **kw):
        if isinstance(store_feedback, AliexpressStoreFeedback):
            for key, value in kw.iteritems():
                setattr(store_feedback, key, value)
            store_feedback.save()
            return True
        return False

    @staticmethod
    def delete(**kw):
        if 'store_id' in kw:
            AliexpressStoreFeedback.objects.filter(**kw).delete()
            return True
        return False

    @staticmethod
    def fetch(**kw):
        return AliexpressStoreFeedback.objects.filter(**kw)

    @staticmethod
    def fetch_one(**kw):
        if 'store_id' in kw:
            try:
                return AliexpressStoreFeedback.objects.get(store_id=kw['store_id'])
            except MultipleObjectsReturned as e:
                logger.error("[ALXSTOREID:{}] Multile aliexpress store feedbacks exist".format(kw['store_id']))
                return None
            except AliexpressStoreFeedback.DoesNotExist as e:
                logger.warning("[ALXSTOREID:{}] No aliexpress store feedback found".format(kw['store_id']))
                return None
        else:
            return None


class AliexpressStoreFeedbackDetailedModelManager(object):

    @staticmethod
    def create(**kw):
        obj = None
        try:
            obj = AliexpressStoreFeedbackDetailed(**kw)
            obj.save()
        except Exception as e:
            logger.error(str(e))
            return None
        return obj

    @staticmethod
    def update(store_feedback_detailed, **kw):
        if isinstance(store_feedback_detailed, AliexpressStoreFeedbackDetailed):
            for key, value in kw.iteritems():
                setattr(store_feedback_detailed, key, value)
            store_feedback_detailed.save()
            return True
        return False

    @staticmethod
    def delete(**kw):
        if 'store_id' in kw:
            AliexpressStoreFeedbackDetailed.objects.filter(**kw).delete()
            return True
        return False

    @staticmethod
    def fetch(**kw):
        return AliexpressStoreFeedbackDetailed.objects.filter(**kw)

    @staticmethod
    def fetch_one(**kw):
        if 'store_id' in kw:
            try:
                return AliexpressStoreFeedbackDetailed.objects.get(store_id=kw['store_id'])
            except MultipleObjectsReturned as e:
                logger.error("[ALXSTOREID:{}] Multile aliexpress store feedback detailed exist".format(kw['store_id']))
                return None
            except AliexpressStoreFeedbackDetailed.DoesNotExist as e:
                logger.warning("[ALXSTOREID:{}] No aliexpress store feedback detailed found".format(kw['store_id']))
                return None
        else:
            return None

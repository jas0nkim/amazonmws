import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'rfi'))

from django.core.exceptions import MultipleObjectsReturned

from amazonmws import settings
from amazonmws.loggers import GrayLogger as logger

from rfi_errors.models import EbayTradingApiError, EbayNotificationError, ErrorEbayInvalidCategory

class EbayTradingApiErrorModelManager(object):

    @staticmethod
    def fetch(**kw):
        return EbayTradingApiError.objects.filter(**kw)

    @staticmethod
    def delete(error_obj):
        if error_obj.__class__.__name__ == 'EbayTradingApiError':
            return error_obj.delete()
        return False


class EbayNotificationErrorModelManager(object):

    @staticmethod
    def fetch(**kw):
        return EbayNotificationError.objects.filter(**kw)

    @staticmethod
    def delete(error_obj):
        if error_obj.__class__.__name__ == 'EbayNotificationError':
            return error_obj.delete()
        return False


class ErrorEbayInvalidCategoryModelManager(object):

    @staticmethod
    def fetch(**kw):
        return ErrorEbayInvalidCategory.objects.filter(**kw)

    @staticmethod
    def delete(error_obj):
        if error_obj.__class__.__name__ == 'ErrorEbayInvalidCategory':
            return error_obj.delete()
        return False


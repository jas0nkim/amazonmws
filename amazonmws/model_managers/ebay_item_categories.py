import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'rfi'))

import datetime

from amazonmws import settings
from amazonmws.loggers import GrayLogger as logger

from rfi_sources.models import EbayItemCategory


class EbayItemCategoryManager(object):

    @staticmethod
    def save(**kw):
        obj, created = EbayItemCategory.objects.update_or_create(**kw)
        return obj


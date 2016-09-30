import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'rfi'))

from django.forms.models import model_to_dict

from amazonmws import django_cli
django_cli.execute()

from amazonmws import settings, utils
from amazonmws.errors import record_notification_error
from amazonmws.loggers import GrayLogger as logger, StaticFieldFilter, get_logger_name
from amazonmws.model_managers import *

from atoe.helpers import OrderShippingTrackingHandler, FeedbackLeavingHandler


def get_item_performances(ebay_store_id, days=3):
    ret = []
    store = EbayStoreModelManager.fetch_one(id=ebay_store_id)
    if not store:
        return ret
    performance_data = EbayItemStatModelManager.fetch_performances_past_days(days=days)
    for performance in performance_data:
        ret.append(performance)
    return ret


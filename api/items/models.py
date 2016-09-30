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
        ebay_item = EbayItemModelManager.fetch_one(ebid=performance.ebid)
        if not ebay_item or ebay_item.ebay_store_id != store.id:
            continue
        performance_dict = model_to_dict(performance)
        performance_dict['item'] = model_to_dict(ebay_item)
        ret.append(performance_dict)
    return ret


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


def get_order_returns(ebay_store_id, start_return_id=0, limit=200):
    _last_return_id = 0
    ret = { 'data': [], 'last_return_id': _last_return_id }
    store = EbayStoreModelManager.fetch_one(id=ebay_store_id)
    if not store:
        return ret
    if int(start_return_id) > 0:
        returns = EbayOrderReturnModelManager.fetch(ebay_store=store, order='return_id', desc=True, limit=limit, return_id__lte=start_return_id)
    else:
        returns = EbayOrderReturnModelManager.fetch(ebay_store=store, order='return_id', desc=True, limit=limit)
    for retrn in returns:
        retrn_dict = model_to_dict(retrn)
        # add ebay order item
        ebay_order_item_dict = None
        ebay_order_item = EbayOrderItemModelManager.fetch_one(transaction_id=retrn.transaction_id)
        if ebay_order_item:
            ebay_order_item_dict = model_to_dict(ebay_order_item)
        retrn_dict['ebay_order_item'] = ebay_order_item_dict
        # add ebay order
        ebay_order_dict = None
        ebay_order = None
        if ebay_order_item:
            ebay_order = EbayOrderModelManager.fetch_one(order_id=ebay_order_item.order_id)
            ebay_order_dict = model_to_dict(ebay_order)
        retrn_dict['ebay_order'] = ebay_order_dict
        # add amazon order, if available
        amazon_order_dict = None
        if ebay_order:
            ordered_pair = EbayOrderAmazonOrderModelManager.fetch_one(ebay_order_id=ebay_order.order_id)
            if ordered_pair:
                amazon_order_dict = model_to_dict(ordered_pair.amazon_order)
                amazon_order_dict['amazon_account_email'] = str(ordered_pair.amazon_order.amazon_account)
        retrn_dict['amazon_order'] = amazon_order_dict
        ret['data'].append(retrn_dict)
        _last_return_id = retrn.return_id
    ret['last_return_id'] = _last_return_id
    return ret

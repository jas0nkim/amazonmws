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


def get_unplaced_orders(ebay_store_id, since_num_days_ago=1):
    ret = []
    store = EbayStoreModelManager.fetch_one(id=ebay_store_id)
    if not store:
        return ret
    
    orders = EbayOrderModelManager.fetch(ebay_store=store, order='record_number', desc=True)
    for order in orders:
        order_dict = model_to_dict(order)
        # add ebay items
        sold_items = []
        for ordered_item in order.ordered_items.all():
            sold_items.append(model_to_dict(ordered_item))
        order_dict['items'] = sold_items
        # add amazon order, if available
        amazon_order = None
        ordered_pair = EbayOrderAmazonOrderModelManager.fetch_one(ebay_order_id=order.order_id)
        if ordered_pair:
            amazon_order = model_to_dict(ordered_pair.amazon_order)
        order_dict['amazon_order'] = amazon_order
        # add order shipping tracking, if available
        tracking = None
        ebay_order_shipping = EbayOrderShippingModelManager.fetch_one(ebay_order_id=order.order_id)
        if ebay_order_shipping:
            tracking = model_to_dict(ebay_order_shipping)
        order_dict['tracking'] = tracking
        ret.append(order_dict)

    return ret

def create_new_amazon_order(amazon_account_id, amazon_order_id, ebay_order_id, asin, item_price, shipping_and_handling, tax, total):

    amazon_order = AmazonOrderModelManager.create(order_id=amazon_order_id,
        asin=asin,
        amazon_account_id=amazon_account_id,
        item_price=item_price,
        shipping_and_handling=shipping_and_handling,
        tax=tax,
        total=total)

    if not amazon_order:
        return False

    return EbayOrderAmazonOrderModelManager.create(amazon_order_id=amazon_order_id, ebay_order_id=ebay_order_id)

def create_new_order_tracking(amazon_order_id, ebay_order_id, carrier, tracking_number):
    ebay_order = EbayOrderModelManager.fetch_one(order_id=ebay_order_id)
    if not ebay_order:
        return False

    ordered_pair = EbayOrderAmazonOrderModelManager.fetch_one(ebay_order_id=ebay_order.order_id)
    if not ordered_pair or not ordered_pair.amazon_order:
        return False

    # insert tracking info into amazon_orders table
    AmazonOrderModelManager.update(amazon_order=ordered_pair.amazon_order,
        carrier=carrier, tracking_number=tracking_number)

    # create new ebay_order_shippings entry
    return EbayOrderShippingModelManager.create(order_id=ebay_order_id,
        carrier=carrier, tracking_number=tracking_number)

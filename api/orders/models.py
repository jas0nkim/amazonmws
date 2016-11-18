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


def get_unplaced_orders(ebay_store_id, start_record_number=0, limit=200):
    _last_record_number = 0
    ret = { 'data': [], 'last_record_number': _last_record_number }
    store = EbayStoreModelManager.fetch_one(id=ebay_store_id)
    if not store:
        return ret
    if start_record_number > 0:
        orders = EbayOrderModelManager.fetch(ebay_store=store, order='record_number', desc=True, limit=limit, record_number__lte=start_record_number)
    else:
        orders = EbayOrderModelManager.fetch(ebay_store=store, order='record_number', desc=True, limit=limit)
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
            amazon_order['amazon_account_email'] = str(ordered_pair.amazon_order.amazon_account)
        order_dict['amazon_order'] = amazon_order
        # add order shipping tracking, if available
        tracking = None
        ebay_order_shipping = EbayOrderShippingModelManager.fetch_one(ebay_order_id=order.order_id)
        if ebay_order_shipping:
            tracking = model_to_dict(ebay_order_shipping)
        order_dict['tracking'] = tracking
        ret['data'].append(order_dict)
        _last_record_number = order.record_number
    ret['last_record_number'] = _last_record_number
    return ret

def update_ebay_order(order_id, feedback_left=True):
    order = EbayOrderModelManager.fetch_one(order_id=order_id)
    if not order:
        return False

    store = EbayStoreModelManager.fetch_one(id=order.ebay_store_id)
    if not store:
        return False

    feedback = FeedbackLeavingHandler(ebay_store=store)
    return feedback.leave_feedback(ebay_order=order)

def create_new_amazon_order(amazon_account_id, amazon_order_id, ebay_order_id, items, item_price, shipping_and_handling, tax, total):

    amazon_order = AmazonOrderModelManager.create(order_id=amazon_order_id,
        amazon_account_id=amazon_account_id,
        item_price=item_price,
        shipping_and_handling=shipping_and_handling,
        tax=tax,
        total=total)

    if not amazon_order:
        return False

    for item in items:
        if 'sku' not in item:
            continue
        amazon_order_item = AmazonOrderItemModelManager.create(amazon_order=amazon_order,
            order_id=amazon_order_id,
            asin=item['sku'],
            is_variation=item['is_variation'] if 'is_variation' in item else False)

    return EbayOrderAmazonOrderModelManager.create(amazon_order_id=amazon_order_id, ebay_order_id=ebay_order_id)

def create_new_order_tracking(ebay_store_id, ebay_order_id, carrier, tracking_number):
    store = EbayStoreModelManager.fetch_one(id=ebay_store_id)
    if not store:
        return False

    tracking_handler = OrderShippingTrackingHandler(ebay_store=store)
    return tracking_handler.set_shipping_tracking_information(ebay_order_id=ebay_order_id,
        carrier=carrier,
        tracking_number=tracking_number
    )

def get_order_reports(ebay_store_id, durationtype='daily'):
    ret = []
    store = EbayStoreModelManager.fetch_one(id=ebay_store_id)
    if not store:
        return ret
    report_data = EbayOrderModelManager.fetch_reports(
        ebay_store_id=ebay_store_id,
        durationtype=durationtype)
    for report in report_data:
        ret.append(report)
    return ret

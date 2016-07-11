import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'rfi'))

###### setting django module ######

os.environ['DJANGO_SETTINGS_MODULE'] = 'rfi.settings'

import django
django.setup()

###################################

from amazonmws import settings, utils
from amazonmws.errors import record_notification_error
from amazonmws.loggers import GrayLogger as logger, StaticFieldFilter, get_logger_name
from amazonmws.model_managers import *

from atoe.actions import EbayOrderAction


from flask import Blueprint, abort, jsonify

order = Blueprint('order', __name__)

@order.route('/', methods=['GET'])
def list():
    try:
        ret = []

        store = EbayStoreModelManager.fetch_one(id=1)
        action = EbayOrderAction(ebay_store=store)
        
        orders = action.get_orders(not_placed_at_origin_only=True)
        for order in orders:
            try:
                sale_record = action.get_sale_record(order_id=order.OrderID)
                if sale_record:
                    sold_items = []
                    for transaction in order.TransactionArray.Transaction:
                        try:
                            ebay_item = EbayItemModelManager.fetch_one(ebid=transaction.Item.ItemID)
                            if ebay_item:
                                sold_items.append({
                                    "item_id": transaction.Item.ItemID,
                                    "item_title": ebay_item.amazon_item.title,
                                    "asin": ebay_item.amazon_item.asin,
                                })
                        except Exception as e:
                            logger.exception("[EBID:{}] Failed to fetch ebay item from internal system - {}".format(transaction.Item.ItemID, str(e)))
                            continue
                    if len(sold_items) < 1:
                        logger.error("[SaleRecordID:{}] No ebay item found from the order - {}".format(sale_record.SaleRecordID, str(e)))
                        continue

                    ret.append({
                        "record_number": sale_record.SaleRecordID,
                        "order_id": order.OrderID,
                        "items": sold_items,
                        "sale_price": sale_record.SalePrice,
                        "total_price": sale_record.TotalAmount,
                        "order_status": sale_record.OrderStatus.PaidTime,
                        "buyer_email": sale_record.BuyerEmail,
                        "buyer_user_id": sale_record.BuyerID,
                        "buyer_status": "",
                        "buyer_shipping_name": "",
                        "buyer_shipping_street1": "",
                        "buyer_shipping_street2": "",
                        "buyer_shipping_city_name": "",
                        "buyer_shipping_state_or_province": "",
                        "buyer_shipping_country": "",
                        "buyer_shipping_country_name": "",
                        "buyer_shipping_phone": "",
                        "buyer_shipping_postal_code": "",
                        "creation_time",
                        "paid_time",
                    })
            except Exception as e:
                logger.exception("Failed to get sale record - {}".format(str(e)))
                continue

        return jsonify(**ret)

    except Exception as e:
        logger.exception("Failed to fetch orders - {}".format(str(e)))
        abort(500)

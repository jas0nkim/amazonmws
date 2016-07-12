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


def get_unplaced_orders(ebay_store_id, since_num_days_ago=1):
    ret = []

    store = EbayStoreModelManager.fetch_one(id=ebay_store_id)
    if not store:
        return ret
    
    action = EbayOrderAction(ebay_store=store)
    orders = action.get_orders(since_num_days_ago=since_num_days_ago, not_placed_at_origin_only=True)
    
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
                    logger.error("[SaleRecordID:{}] No ebay item found from the order - {}".format(sale_record.SaleRecordID))
                    continue

                ret.append({
                    "record_number": sale_record.SaleRecordID,
                    "order_id": order.OrderID,
                    "items": sold_items,
                    "total_price": sale_record.TotalAmount,
                    "shipping_cost": sale_record.ActualShippingCost,
                    "buyer_email": sale_record.BuyerEmail,
                    "buyer_user_id": sale_record.BuyerID,
                    "buyer_status": "",
                    "buyer_shipping_name": sale_record.ShippingAddress.Name,
                    "buyer_shipping_street1": sale_record.ShippingAddress.Street1,
                    "buyer_shipping_street2": sale_record.ShippingAddress.get('Street2', ''), # optional
                    "buyer_shipping_city_name": sale_record.ShippingAddress.CityName,
                    "buyer_shipping_state_or_province": sale_record.ShippingAddress.StateOrProvince,
                    "buyer_shipping_postal_code": sale_record.ShippingAddress.PostalCode,
                    "buyer_shipping_country": sale_record.ShippingAddress.Country,
                    "buyer_shipping_phone": sale_record.ShippingAddress.get('Phone', ''), # optional
                    "checkout_status": sale_record.OrderStatus.CheckoutStatus,
                    "creation_time": sale_record.CreationTime,
                    "paid_time": sale_record.OrderStatus.get('PaidTime', ''), # optional
                })
        except Exception as e:
            logger.exception("Failed to get sale record - {}".format(str(e)))
            continue
    return ret

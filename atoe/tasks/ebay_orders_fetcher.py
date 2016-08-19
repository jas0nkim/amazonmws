import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'scrapers', 'amzn'))

import getopt

from amazonmws import django_cli
django_cli.execute()

from amazonmws import settings as amazonmws_settings, utils as amazonmws_utils
from amazonmws.loggers import GrayLogger as logger
from amazonmws.model_managers import *

from atoe.actions import EbayOrderAction


__ebay_stores = [1, ]

def __fetch_and_save_orders(ebay_store, since_num_days_ago=1):
    action = EbayOrderAction(ebay_store=ebay_store)
    orders = action.get_orders(since_num_days_ago=since_num_days_ago, not_placed_at_origin_only=True)
    
    for order in orders:
        try:
            # check order already stored in db
            _existed_order = EbayOrderModelManager.fetch_one(order_id=order.OrderID)
            if _existed_order:
                continue

            sale_record = action.get_sale_record(order_id=order.OrderID)
            if sale_record:
                sold_items = []
                for transaction in order.TransactionArray.Transaction:
                    sold_items.append({
                        "order_id": order.OrderID,
                        "ebid": transaction.Item.ItemID,
                        "transaction_id": transaction.TransactionID,
                        "title": transaction.Item.get('Title', ''),
                        "sku": transaction.Item.get('SKU', ''),
                        "quantity": transaction.get('QuantityPurchased', ''),
                        "price": transaction.TransactionPrice.get('value', 0.00),
                    })
                
                if len(sold_items) < 1:
                    logger.error("[SaleRecordID:{}] No ebay item found from the order - {}".format(sale_record.SaleRecordID))
                    continue

                # init/create ebay order
                ebay_order = EbayOrderModelManager.create(ebay_store=ebay_store,
                    order_id=order.OrderID,
                    record_number=sale_record.SaleRecordID,
                    total_price=sale_record.TotalAmount.get('value', 0.00),
                    shipping_cost=sale_record.ActualShippingCost.get('value', 0.00),
                    buyer_email=sale_record.BuyerEmail,
                    buyer_user_id=sale_record.BuyerID,
                    buyer_status=None,
                    buyer_shipping_name=sale_record.ShippingAddress.Name,
                    buyer_shipping_street1=sale_record.ShippingAddress.Street1,
                    buyer_shipping_street2=sale_record.ShippingAddress.get('Street2', ''), # optional
                    buyer_shipping_city_name=sale_record.ShippingAddress.CityName,
                    buyer_shipping_state_or_province=sale_record.ShippingAddress.StateOrProvince,
                    buyer_shipping_postal_code=sale_record.ShippingAddress.PostalCode,
                    buyer_shipping_country=sale_record.ShippingAddress.Country,
                    buyer_shipping_phone=sale_record.ShippingAddress.get('Phone', ''), # optional
                    checkout_status=sale_record.OrderStatus.CheckoutStatus,
                    creation_time=sale_record.CreationTime,
                    paid_time=sale_record.OrderStatus.get('PaidTime', '') # optional
                )

                # enter ebay items for order
                for sold_item in sold_items:
                    sold_item['ebay_order'] = ebay_order
                    EbayOrderItemModelManager.create(**sold_item)

        except Exception as e:
            logger.exception("Failed to save ebay order - {}".format(str(e)))
            continue


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "h:")
    except getopt.GetoptError:
        print 'ebay_orders_fetcher.py'
        sys.exit(2)
    
    for opt, arg in opts:
        if opt == '-h':
            print 'ebay_orders_fetcher.py'
            sys.exit()
    run()

def run():
    for ebay_store_id in __ebay_stores:
        ebay_store = EbayStoreModelManager.fetch_one(id=ebay_store_id)
        if not ebay_store:
            continue
        __fetch_and_save_orders(ebay_store)


if __name__ == "__main__":
    main(sys.argv[1:])

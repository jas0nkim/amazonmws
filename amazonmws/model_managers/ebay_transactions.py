import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

import datetime

from storm.expr import Select, And, Desc
from storm.exceptions import StormError

from amazonmws import settings, utils
from amazonmws.models import StormStore, EbayStore, EbayItem, Transaction, TransactionAmazonOrder, AmazonOrder, zzAmazonItem as AmazonItem, zzAmazonItemPicture as AmazonItemPicture, zzAtoECategoryMap as AtoECategoryMap, zzAmazonItemOffer as AmazonItemOffer, zzAmazonBestsellers as AmazonBestsellers,zzEbayStorePreferredCategory as EbayStorePreferredCategory
from amazonmws.loggers import GrayLogger as logger


class TransactionModelManager(object):

    @staticmethod
    def create(ebay_store_id, recipient_user_id, item_id, transaction_data, item=None, transaction_array=None, raw=None):
        try:
            trans = Transaction()
            trans.ebay_store_id = ebay_store_id
            trans.seller_user_id = recipient_user_id
            trans.transaction_id = transaction_data["TransactionID"]
            trans.item_id = item_id
            trans.order_id = transaction_data["ContainingOrder"]["OrderID"]
            trans.external_transaction_id = transaction_data["ExternalTransaction"]["ExternalTransactionID"] if "ExternalTransactionID" in transaction_data["ExternalTransaction"] else None
            trans.transaction_price = utils.number_to_dcmlprice(transaction_data["TransactionPrice"])
            trans.sales_tax_percent = utils.number_to_dcmlprice(transaction_data["ShippingDetails"]["SalesTax"]["SalesTaxPercent"]) if "SalesTaxPercent" in transaction_data["ShippingDetails"]["SalesTax"] else None
            trans.sales_tax_state = transaction_data["ShippingDetails"]["SalesTax"]["SalesTaxState"] if "SalesTaxState" in transaction_data["ShippingDetails"]["SalesTax"] else None
            trans.sales_tax_amount = trans.transaction_price * trans.sales_tax_percent / utils.number_to_dcmlprice('100.0') # because given number is CAD... don't know why...
            trans.amount_paid = utils.number_to_dcmlprice(transaction_data["AmountPaid"])
            trans.buyer_email = transaction_data["Buyer"]["Email"] if "Email" in transaction_data["Buyer"] else None
            trans.buyer_user_id = transaction_data["Buyer"]["UserID"]
            trans.buyer_status = transaction_data["Buyer"]["Status"]
            trans.buyer_shipping_name = transaction_data["Buyer"]["BuyerInfo"]["ShippingAddress"]["Name"]
            trans.buyer_shipping_street1 = transaction_data["Buyer"]["BuyerInfo"]["ShippingAddress"]["Street1"] if "Street1" in transaction_data["Buyer"]["BuyerInfo"]["ShippingAddress"] else None
            trans.buyer_shipping_street2 = transaction_data["Buyer"]["BuyerInfo"]["ShippingAddress"]["Street2"] if "Street2" in transaction_data["Buyer"]["BuyerInfo"]["ShippingAddress"] else None
            trans.buyer_shipping_city_name = transaction_data["Buyer"]["BuyerInfo"]["ShippingAddress"]["CityName"] if "CityName" in transaction_data["Buyer"]["BuyerInfo"]["ShippingAddress"] else None
            trans.buyer_shipping_state_or_province = transaction_data["Buyer"]["BuyerInfo"]["ShippingAddress"]["StateOrProvince"] if "StateOrProvince" in transaction_data["Buyer"]["BuyerInfo"]["ShippingAddress"] else None
            trans.buyer_shipping_country = transaction_data["Buyer"]["BuyerInfo"]["ShippingAddress"]["Country"] if "Country" in transaction_data["Buyer"]["BuyerInfo"]["ShippingAddress"] else None
            trans.buyer_shipping_country_name = transaction_data["Buyer"]["BuyerInfo"]["ShippingAddress"]["CountryName"] if "CountryName" in transaction_data["Buyer"]["BuyerInfo"]["ShippingAddress"] else None
            trans.buyer_shipping_phone = transaction_data["Buyer"]["BuyerInfo"]["ShippingAddress"]["Phone"] if "Phone" in transaction_data["Buyer"]["BuyerInfo"]["ShippingAddress"] else None
            trans.buyer_shipping_postal_code = transaction_data["Buyer"]["BuyerInfo"]["ShippingAddress"]["PostalCode"] if "PostalCode" in transaction_data["Buyer"]["BuyerInfo"]["ShippingAddress"] else None
            trans.order_status = transaction_data["ContainingOrder"]["OrderStatus"]
            trans.ebay_payment_status = transaction_data["Status"]["eBayPaymentStatus"] if "eBayPaymentStatus" in transaction_data["Status"] else None
            trans.checkout_status = transaction_data["Status"]["CheckoutStatus"] if "CheckoutStatus" in transaction_data["Status"] else None
            trans.complete_status = transaction_data["Status"]["CompleteStatus"] if "CompleteStatus" in transaction_data["Status"] else None
            trans.payment_hold_status = transaction_data["Status"]["PaymentHoldStatus"] if "PaymentHoldStatus" in transaction_data["Status"] else None
            trans.external_transaction_status = transaction_data["Status"]["ExternalTransactionStatus"] if "ExternalTransactionStatus" in transaction_data["Status"] else None
            trans.raw_item = item
            trans.raw_transactionarray = transaction_array
            trans.raw_xml = raw
            trans.created_at = datetime.datetime.now()
            trans.updated_at = datetime.datetime.now()
            
            StormStore.add(trans)
            StormStore.commit()
            return trans
        except StormError:
            logger.exception("Failed to store data")
            StormStore.rollback()
            return False
        except Exception as e:
            logger.exception(e)
            StormStore.rollback()
            return False

    @staticmethod
    def fetch(**kw):
        expressions = []
        if 'ebay_store_id' in kw:
            expressions += [ Transaction.ebay_store_id == kw['ebay_store_id'] ]
        elif 'seller_user_id' in kw:
            expressions += [ Transaction.seller_user_id == kw['seller_user_id'] ]
        if 'since' in kw:
            expressions += [ Transaction.created_at >= kw['since'] ]

        if len(expressions) > 0:
            result_set = StormStore.find(Transaction, And(*expressions))
        else:
            result_set = StormStore.find(Transaction)

        # order by
        if 'order_by' in kw:
            if 'order_desc' in kw and kw['order_desc']:
                return result_set.order_by(Desc(getattr(Transaction, kw['order_by'])))
            else:
                return result_set.order_by(getattr(Transaction, kw['order_by']))
        return result_set

    @staticmethod
    def fetch_not_ordered(since):
        ret = []
        transactions = StormStore.find(Transaction, Transaction.created_at >= since)
        for transaction in transactions:
            try:
                tao = StormStore.find(TransactionAmazonOrder,
                    TransactionAmazonOrder.transaction_id == transaction.id).one()
                if not tao:
                    ret.append(transaction)
                else:
                    continue

            except StormError:
                ret.append(transaction)

        return ret


    @staticmethod
    def fetch_one_transaction_amazon_order_or_create(transaction_id):
        try:
            trans_am_order = StormStore.find(TransactionAmazonOrder, TransactionAmazonOrder.transaction_id == transaction_id).one()
            
            if not trans_am_order:
                trans_am_order = TransactionAmazonOrder()
                trans_am_order.transaction_id = transaction_id
                trans_am_order.created_at = datetime.datetime.now()
                trans_am_order.updated_at = datetime.datetime.now()

                StormStore.add(trans_am_order)
                StormStore.commit()

            return trans_am_order

        except StormError:
            logger.exception("Failed to fetch an transaction amazon order")
            return None

    @staticmethod
    def update_transaction_amazon_order(trans_am_order, **kw):
        try:
            trans_am_order.amazon_order_id = kw['amazon_order_id'] if 'amazon_order_id' in kw else trans_am_order.amazon_order_id
            trans_am_order.internal_error_type = kw['internal_error_type'] if 'internal_error_type' in kw else trans_am_order.internal_error_type
            trans_am_order.internal_error_message = kw['internal_error_message'] if 'internal_error_message' in kw else trans_am_order.internal_error_message
            trans_am_order.is_ordering_in_process = kw['is_ordering_in_process'] if 'is_ordering_in_process' in kw else trans_am_order.is_ordering_in_process
            trans_am_order.updated_at = datetime.datetime.now()

            StormStore.add(trans_am_order)
            StormStore.commit()

            return True

        except StormError:
            logger.exception("Failed to fetch an transaction amazon order")
            return None

    @staticmethod
    def start_transaction_amazon_order_process(trans_am_order):
        return TransactionModelManager.update_transaction_amazon_order(trans_am_order, 
            is_ordering_in_process=1)

    @staticmethod
    def end_transaction_amazon_order_process(trans_am_order):
        return TransactionModelManager.update_transaction_amazon_order(trans_am_order, 
            is_ordering_in_process=0)

    @staticmethod
    def create_amazon_order(**kw):
        try:
            amazon_order = AmazonOrder()
            amazon_order.order_id = kw['order_id'] if 'order_id' in kw else None
            amazon_order.asin = kw['asin'] if 'asin' in kw else None
            amazon_order.amazon_account_id = kw['amazon_account_id'] if 'amazon_account_id' in kw else None
            amazon_order.item_price = kw['item_price'] if 'item_price' in kw else None
            amazon_order.shipping_and_handling = kw['shipping_and_handling'] if 'shipping_and_handling' in kw else None
            amazon_order.tax = kw['tax'] if 'tax' in kw else None
            amazon_order.total = kw['total'] if 'total' in kw else None
            amazon_order.buyer_shipping_name = kw['buyer_shipping_name'] if 'buyer_shipping_name' in kw else None
            amazon_order.buyer_shipping_street1 = kw['buyer_shipping_street1'] if 'buyer_shipping_street1' in kw else None
            amazon_order.buyer_shipping_street2 = kw['buyer_shipping_street2'] if 'buyer_shipping_street2' in kw else None
            amazon_order.buyer_shipping_city_name = kw['buyer_shipping_city_name'] if 'buyer_shipping_city_name' in kw else None
            amazon_order.buyer_shipping_state_or_province = kw['buyer_shipping_state_or_province'] if 'buyer_shipping_state_or_province' in kw else None
            amazon_order.buyer_shipping_country = kw['buyer_shipping_country'] if 'buyer_shipping_country' in kw else None
            amazon_order.buyer_shipping_phone = kw['buyer_shipping_phone'] if 'buyer_shipping_phone' in kw else None
            amazon_order.buyer_shipping_postal_code = kw['buyer_shipping_postal_code'] if 'buyer_shipping_postal_code' in kw else None
            amazon_order.carrier = kw['carrier'] if 'carrier' in kw else None
            amazon_order.tracking_number = kw['tracking_number'] if 'tracking_number' in kw else None
            amazon_order.created_at = datetime.datetime.now()
            amazon_order.updated_at = datetime.datetime.now()

            StormStore.add(amazon_order)
            StormStore.commit()

            return amazon_order

        except StormError:
            logger.exception("Failed to create an amazon order")
            return None


    @staticmethod
    def fetch_amazon_order(transaction_id):
        pass
        
        # try:
        #     trans_am_order = TransactionModelManager.fetch_or_create_trans_amazon_order(id=transaction_id)
            
        #     if not trans_am_order.amazon_order_id:
        #         return trans_am_order

        #     else:
        #         return StormStore.find(AmazonOrder, AmazonOrder.id == trans_am_order.amazon_order_id).one()

        # except StormError:
        #     logger.exception("Failed to fetch an amazon order")
        #     return None

import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

import datetime

from storm.expr import Select, And, Desc
from storm.exceptions import StormError

from amazonmws import settings, utils
from amazonmws.models import StormStore, EbayStore, EbayItem, Transaction, zzAmazonItem as AmazonItem, zzAmazonItemPicture as AmazonItemPicture, zzAtoECategoryMap as AtoECategoryMap, zzAmazonItemOffer as AmazonItemOffer, zzAmazonBestsellers as AmazonBestsellers,zzEbayStorePreferredCategory as EbayStorePreferredCategory
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
            return True
        except StormError:
            logger.exception("Failed to store data")
            StormStore.rollback()
            return False
        except Exception, e:
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

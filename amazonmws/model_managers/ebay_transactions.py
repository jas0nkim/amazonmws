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
            trans.seller_user_id = RecipientUserID
            trans.transaction_id = Transaction_data["TransactionID"]
            trans.item_id = Item_data["ItemID"]
            trans.order_id = Transaction_data["ContainingOrder"]["OrderID"]
            trans.external_transaction_id = Transaction_data["ExternalTransaction"]["ExternalTransactionID"] if "ExternalTransactionID" in Transaction_data["ExternalTransaction"] else None
            trans.transaction_price = utils.number_to_dcmlprice(Transaction_data["TransactionPrice"])
            trans.sales_tax_percent = utils.number_to_dcmlprice(Transaction_data["ShippingDetails"]["SalesTax"]["SalesTaxPercent"]) if "SalesTaxPercent" in Transaction_data["ShippingDetails"]["SalesTax"] else None
            trans.sales_tax_state = Transaction_data["ShippingDetails"]["SalesTax"]["SalesTaxState"] if "SalesTaxState" in Transaction_data["ShippingDetails"]["SalesTax"] else None
            trans.sales_tax_amount = trans.transaction_price * trans.sales_tax_percent / utils.number_to_dcmlprice('100.0') # because given number is CAD... don't know why...
            trans.amount_paid = utils.number_to_dcmlprice(Transaction_data["AmountPaid"])
            trans.buyer_email = Transaction_data["Buyer"]["Email"] if "Email" in Transaction_data["Buyer"] else None
            trans.buyer_user_id = Transaction_data["Buyer"]["UserID"]
            trans.buyer_status = Transaction_data["Buyer"]["Status"]
            trans.buyer_shipping_name = Transaction_data["Buyer"]["BuyerInfo"]["ShippingAddress"]["Name"]
            trans.buyer_shipping_street1 = Transaction_data["Buyer"]["BuyerInfo"]["ShippingAddress"]["Street1"] if "Street1" in Transaction_data["Buyer"]["BuyerInfo"]["ShippingAddress"] else None
            trans.buyer_shipping_street2 = Transaction_data["Buyer"]["BuyerInfo"]["ShippingAddress"]["Street2"] if "Street2" in Transaction_data["Buyer"]["BuyerInfo"]["ShippingAddress"] else None
            trans.buyer_shipping_city_name = Transaction_data["Buyer"]["BuyerInfo"]["ShippingAddress"]["CityName"] if "CityName" in Transaction_data["Buyer"]["BuyerInfo"]["ShippingAddress"] else None
            trans.buyer_shipping_state_or_province = Transaction_data["Buyer"]["BuyerInfo"]["ShippingAddress"]["StateOrProvince"] if "StateOrProvince" in Transaction_data["Buyer"]["BuyerInfo"]["ShippingAddress"] else None
            trans.buyer_shipping_country = Transaction_data["Buyer"]["BuyerInfo"]["ShippingAddress"]["Country"] if "Country" in Transaction_data["Buyer"]["BuyerInfo"]["ShippingAddress"] else None
            trans.buyer_shipping_country_name = Transaction_data["Buyer"]["BuyerInfo"]["ShippingAddress"]["CountryName"] if "CountryName" in Transaction_data["Buyer"]["BuyerInfo"]["ShippingAddress"] else None
            trans.buyer_shipping_phone = Transaction_data["Buyer"]["BuyerInfo"]["ShippingAddress"]["Phone"] if "Phone" in Transaction_data["Buyer"]["BuyerInfo"]["ShippingAddress"] else None
            trans.buyer_shipping_postal_code = Transaction_data["Buyer"]["BuyerInfo"]["ShippingAddress"]["PostalCode"] if "PostalCode" in Transaction_data["Buyer"]["BuyerInfo"]["ShippingAddress"] else None
            trans.order_status = Transaction_data["ContainingOrder"]["OrderStatus"]
            trans.ebay_payment_status = Transaction_data["Status"]["eBayPaymentStatus"] if "eBayPaymentStatus" in Transaction_data["Status"] else None
            trans.checkout_status = Transaction_data["Status"]["CheckoutStatus"] if "CheckoutStatus" in Transaction_data["Status"] else None
            trans.complete_status = Transaction_data["Status"]["CompleteStatus"] if "CompleteStatus" in Transaction_data["Status"] else None
            trans.payment_hold_status = Transaction_data["Status"]["PaymentHoldStatus"] if "PaymentHoldStatus" in Transaction_data["Status"] else None
            trans.external_transaction_status = Transaction_data["Status"]["ExternalTransactionStatus"] if "ExternalTransactionStatus" in Transaction_data["Status"] else None
            trans.raw_item = Item
            trans.raw_transactionarray = TransactionArray
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

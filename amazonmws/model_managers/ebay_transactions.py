import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'rfi'))

from django.core.exceptions import MultipleObjectsReturned

from amazonmws import settings, utils
from amazonmws.loggers import GrayLogger as logger

from rfi_orders.models import Transaction, AmazonOrder
# from rfi_orders.models import Transaction, AmazonOrder, TransactionAmazonOrder
from rfi_account_profiles.models import EbayStore


class TransactionModelManager(object):

    @staticmethod
    def create(ebay_store_id, recipient_user_id, item_id, transaction_data, item=None, transaction_array=None, raw=None):
        _transaction_price = utils.number_to_dcmlprice(transaction_data["TransactionPrice"])
        _sales_tax_percent = utils.number_to_dcmlprice(transaction_data["ShippingDetails"]["SalesTax"]["SalesTaxPercent"]) if "SalesTaxPercent" in transaction_data["ShippingDetails"]["SalesTax"] else None

        kw = {
            'ebay_store_id': ebay_store_id,
            'seller_user_id': recipient_user_id,
            'transaction_id': transaction_data["TransactionID"],
            'item_id': item_id,
            'order_id': transaction_data["ContainingOrder"]["OrderID"],
            'external_transaction_id': transaction_data["ExternalTransaction"]["ExternalTransactionID"] if "ExternalTransactionID" in transaction_data["ExternalTransaction"] else None,
            'transaction_price': _transaction_price,
            'sales_tax_percent': _sales_tax_percent,
            'sales_tax_state': transaction_data["ShippingDetails"]["SalesTax"]["SalesTaxState"] if "SalesTaxState" in transaction_data["ShippingDetails"]["SalesTax"] else None,
            'sales_tax_amount': _transaction_price * _sales_tax_percent / utils.number_to_dcmlprice('100.0'), # because given number is CAD... don't know why...
            'amount_paid': utils.number_to_dcmlprice(transaction_data["AmountPaid"]),
            'buyer_email': transaction_data["Buyer"]["Email"] if "Email" in transaction_data["Buyer"] else None,
            'buyer_user_id': transaction_data["Buyer"]["UserID"],
            'buyer_status': transaction_data["Buyer"]["Status"],
            'buyer_shipping_name': transaction_data["Buyer"]["BuyerInfo"]["ShippingAddress"]["Name"],
            'buyer_shipping_street1': transaction_data["Buyer"]["BuyerInfo"]["ShippingAddress"]["Street1"] if "Street1" in transaction_data["Buyer"]["BuyerInfo"]["ShippingAddress"] else None,
            'buyer_shipping_street2': transaction_data["Buyer"]["BuyerInfo"]["ShippingAddress"]["Street2"] if "Street2" in transaction_data["Buyer"]["BuyerInfo"]["ShippingAddress"] else None,
            'buyer_shipping_city_name': transaction_data["Buyer"]["BuyerInfo"]["ShippingAddress"]["CityName"] if "CityName" in transaction_data["Buyer"]["BuyerInfo"]["ShippingAddress"] else None,
            'buyer_shipping_state_or_province': transaction_data["Buyer"]["BuyerInfo"]["ShippingAddress"]["StateOrProvince"] if "StateOrProvince" in transaction_data["Buyer"]["BuyerInfo"]["ShippingAddress"] else None,
            'buyer_shipping_country': transaction_data["Buyer"]["BuyerInfo"]["ShippingAddress"]["Country"] if "Country" in transaction_data["Buyer"]["BuyerInfo"]["ShippingAddress"] else None,
            'buyer_shipping_country_name': transaction_data["Buyer"]["BuyerInfo"]["ShippingAddress"]["CountryName"] if "CountryName" in transaction_data["Buyer"]["BuyerInfo"]["ShippingAddress"] else None,
            'buyer_shipping_postal_code': transaction_data["Buyer"]["BuyerInfo"]["ShippingAddress"]["PostalCode"] if "PostalCode" in transaction_data["Buyer"]["BuyerInfo"]["ShippingAddress"] else None,
            'order_status': transaction_data["ContainingOrder"]["OrderStatus"],
            'ebay_payment_status': transaction_data["Status"]["eBayPaymentStatus"] if "eBayPaymentStatus" in transaction_data["Status"] else None,
            'checkout_status': transaction_data["Status"]["CheckoutStatus"] if "CheckoutStatus" in transaction_data["Status"] else None,
            'complete_status': transaction_data["Status"]["CompleteStatus"] if "CompleteStatus" in transaction_data["Status"] else None,
            'payment_hold_status': transaction_data["Status"]["PaymentHoldStatus"] if "PaymentHoldStatus" in transaction_data["Status"] else None,
            'external_transaction_status': transaction_data["Status"]["ExternalTransactionStatus"] if "ExternalTransactionStatus" in transaction_data["Status"] else None,
            'raw_item': item,
            'raw_transactionarray': transaction_array,
            'raw_xml': raw,
        }

        obj, created = Transaction.objects.update_or_create(**kw)
        return created

    @staticmethod
    def fetch(**kw):
        # make compatible with django query
        if 'since' in kw:
            kw['created_at__gte'] = kw['since']
            del kw['since']

        transactions = Transaction.objects.filter(**kw)

        # order by
        if 'order_by' in kw:
            if 'order_desc' in kw and kw['order_desc']:
                transactions = transactions.order_by('-{}'.format(kw['order_by']))
            else:
                transactions = transactions.order_by(kw['order_by'])
        
        return transactions

    @staticmethod
    def fetch_not_ordered(since):
        return []

        # ret = []
        # transactions = Transaction.objects.filter(created_at__gte=since)
        # for transaction in transactions:
        #     try:
        #         tao = TransactionAmazonOrder.objects.get(transaction=transaction)
        #         if not tao:
        #             ret.append(transaction)
        #         else:
        #             continue
        #     except MultipleObjectsReturned as e:
        #         logger.error("[TransID:%s] Multiple transaction exists in the system" % transaction.id)
        #         continue
        #     except TransactionAmazonOrder.DoesNotExist as e:
        #         ret.append(transaction)
        
        # return ret

    @staticmethod
    def fetch_not_tracked(since):
        ret = []
        transactions = Transaction.objects.filter(created_at__gte=since)
        for transaction in transactions:
            try:
                if not transaction.carrier or not transaction.tracking_number:
                    ret.append(transaction)
                else:
                    continue
            except Exception:
                ret.append(transaction)

        return ret

    @staticmethod
    def fetch_one(**kw):
        if 'id' in kw:
            try:
                return Transaction.objects.get(id=kw['id'])
            except MultipleObjectsReturned as e:
                logger.error("[TransID:%s] Multiple transaction id exists in the system" % kw['id'])
                return None
            except Transaction.DoesNotExist as e:
                logger.warning("[TransID:%s] Transaction id not exists in the system" % kw['id'])
                return None
        elif 'order_id' in kw:
            try:
                return Transaction.objects.get(order_id=kw['order_id'])
            except MultipleObjectsReturned as e:
                logger.error("[OrderID:%s] Multiple order id exists in the system" % kw['order_id'])
                return None
            except Transaction.DoesNotExist as e:
                logger.warning("[OrderID:%s] Order id not exists in the system" % kw['order_id'])
                return None
        else:
            return None

    @staticmethod
    def fetch_one_transaction_amazon_order_or_create(transaction_id):
        return None

        # trans_am_order, created = TransactionAmazonOrder.objects.get_or_create(transaction_id=transaction_id)
        # return trans_am_order

    @staticmethod
    def update_transaction_amazon_order(trans_am_order, **kw):
        return False

        # if isinstance(trans_am_order, TransactionAmazonOrder):
        #     for key, value in kw.iteritems():
        #         setattr(trans_am_order, key, value)
        #     trans_am_order.save()
        #     return True
        # return False

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
        amazon_order, created = AmazonOrder.objects.update_or_create(**kw)
        return amazon_order

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

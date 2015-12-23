import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from amazonmws import settings as amazonmws_settings, utils as amazonmws_utils
from amazonmws.loggers import GrayLogger as logger, StaticFieldFilter, get_logger_name
from amazonmws.models import AmazonOrder, TransactionAmazonOrder
from amazonmws.model_managers import *

from automatic.amazon.ordering import AmazonOrdering


class AmazonOrderingHandler(object):

    transaction_amazon_order = None

    def __init__(self, ebay_store, ebay_transaction, asin):
        self.ebay_store = ebay_store
        self.ebay_transaction = ebay_transaction
        self.asin = asin
        self.amazon_account = AmazonAccountModelManager.fetch_one(ebay_store_id=ebay_store.id)
        self.transaction_amazon_order = TransactionModelManager.fetch_one_transaction_amazon_order_or_create(transaction_id=ebay_transaction.id)

        logger.addFilter(StaticFieldFilter(get_logger_name(), 'amazon_ordering'))

    def _proceed(self):
        try:
            TransactionModelManager.start_transaction_amazon_order_process(self.transaction_amazon_order)

            ordering = AmazonOrdering(asin=self.asin,
                ebay_order_id=self.ebay_transaction.order_id,
                amazon_user=self.amazon_account.email,
                amazon_pass=self.amazon_account.password,
                billing_addr_zip=self.amazon_account.billing_postal,
                buyer_fullname=self.ebay_transaction.buyer_shipping_name,
                buyer_shipping_address1=self.ebay_transaction.buyer_shipping_street1,
                buyer_shipping_address2=self.ebay_transaction.buyer_shipping_street2,
                buyer_shipping_city=self.ebay_transaction.buyer_shipping_city_name,
                buyer_shipping_state=self.ebay_transaction.buyer_shipping_state_or_province,
                buyer_shipping_postal=self.ebay_transaction.buyer_shipping_postal_code,
                buyer_shipping_phone=self.ebay_transaction.buyer_shipping_phone)
            ordering.run()

            if not ordering.order_number:
                return TransactionModelManager.update_transaction_amazon_order(
                    self.transaction_amazon_order, 
                    internal_error_type=ordering.error_type, 
                    internal_error_message=amazonmws_utils.str_to_unicode(ordering.error_message))
            else:
                amazon_order = TransactionModelManager.create_amazon_order(
                    order_id=ordering.order_number,
                    asin=self.asin,
                    amazon_account_id=self.amazon_account.id,
                    item_price=ordering.item_price,
                    shipping_and_handling=ordering.shipping_and_handling,
                    tax=ordering.tax,
                    total=ordering.total,
                    buyer_shipping_name=self.ebay_transaction.buyer_shipping_name,
                    buyer_shipping_street1=self.ebay_transaction.buyer_shipping_street1,
                    buyer_shipping_street2=self.ebay_transaction.buyer_shipping_street2,
                    buyer_shipping_city_name=self.ebay_transaction.buyer_shipping_city_name,
                    buyer_shipping_state_or_province=self.ebay_transaction.buyer_shipping_state_or_province,
                    buyer_shipping_country=self.ebay_transaction.buyer_shipping_country,
                    buyer_shipping_phone=self.ebay_transaction.buyer_shipping_phone,
                    buyer_shipping_postal_code=self.ebay_transaction.buyer_shipping_postal_code)

                return TransactionModelManager.update_transaction_amazon_order(
                    self.transaction_amazon_order, 
                    amazon_order_id=amazon_order.id)
        
        finally:
            TransactionModelManager.end_transaction_amazon_order_process(self.transaction_amazon_order)


    def run(self):
        if self.transaction_amazon_order and not self.transaction_amazon_order.amazon_order_id and not self.transaction_amazon_order.is_ordering_in_process:

            logger.info('[{}] proceed ordering'.format(self.ebay_transaction.order_id))

            # start process
            return self._proceed()
        
        else:
            if not self.transaction_amazon_order:
                logger.info('[{}] invalid transaction id'.format(self.ebay_transaction.order_id))
                return False
            
            if self.transaction_amazon_order.is_ordering_in_process:
                logger.info('[{}] amazon ordering is in process by another'.format(self.ebay_transaction.order_id))
                return False

            if self.transaction_amazon_order.amazon_order_id:
                logger.info('[{}] already has amazon order - {}'.format(self.ebay_transaction.order_id, self.transaction_amazon_order.amazon_order_id))
                return False

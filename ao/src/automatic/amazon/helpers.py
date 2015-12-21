import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from amazonmws import settings as amazonmws_settings, utils as amazonmws_utils
from amazonmws.loggers import GrayLogger as logger, StaticFieldFilter, get_logger_name
from amazonmws.model_managers import *

from automatic.amazon.ordering import AmazonOrdering


class AmazonOrderingHandler(object):

    def __init__(self, ebay_store, ebay_transaction, asin):
        self.ebay_store = ebay_store
        self.ebay_transaction = ebay_transaction
        self.asin = asin
        self.amazon_account = AmazonAccountModelManager.fetch_one(ebay_store_id=ebay_store.id)

    def run(self):
        auto_ordering = AmazonOrdering(asin=self.asin,
            amazon_user=amazon_account.email,
            amazon_pass=amazon_account.password,
            billing_addr_zip=amazon_account.billing_postal,
            buyer_fullname=ebay_transaction.buyer_shipping_name,
            buyer_shipping_address1=ebay_transaction.buyer_shipping_street1,
            buyer_shipping_address2=ebay_transaction.buyer_shipping_street2,
            buyer_shipping_city=ebay_transaction.buyer_shipping_city_name,
            buyer_shipping_state=ebay_transaction.buyer_shipping_state_or_province,
            buyer_shipping_postal=ebay_transaction.buyer_shipping_postal_code,
            buyer_shipping_phone=ebay_transaction.buyer_shipping_phone)
        auto_ordering.run()
        
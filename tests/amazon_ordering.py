import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'ao', 'src'))

from storm.exceptions import StormError

from amazonmws import settings, utils
from amazonmws.loggers import GrayLogger as logger, StaticFieldFilter, get_logger_name
from amazonmws.model_managers import *

from automatic.amazon.helpers import AmazonOrderingHandler


if __name__ == "__main__":

	ebay_store = EbayStoreModelManager.fetch_one(username='redflagitems777')
	transaction = TransactionModelManager.fetch(ebay_store_id=1).one()
	asin = 'B003IG8RQW'

	ordering_handler = AmazonOrderingHandler(ebay_store, transaction, asin)
	ordering_handler.run()

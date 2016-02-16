import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'rfi'))
# sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'tasks'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'ao', 'src'))

###### setting django module ######

os.environ['DJANGO_SETTINGS_MODULE'] = 'rfi.settings'

import django
django.setup()

###################################

# from clry_tasks import automations

from amazonmws.model_managers import *
from automatic.amazon.helpers import AmazonOrderingHandler



if __name__ == "__main__":

    # automations.ordering_task.delay(3205)

    transaction_id = 3205

    transaction = TransactionModelManager.fetch_one(id=transaction_id)
    ebay_store = EbayStoreModelManager.fetch_one(username=transaction.seller_user_id)
    ebay_item = EbayItemModelManager.fetch_one(ebid=transaction.item_id)

    ordering_handler = AmazonOrderingHandler(ebay_store=ebay_store, ebay_transaction=transaction, asin=ebay_item.asin)
    ordering_handler.run()

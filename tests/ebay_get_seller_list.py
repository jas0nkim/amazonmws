import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from amazonmws.model_managers import *
from atoe.actions import EbayItemAction

if __name__ == "__main__":

    store = EbayStoreModelManager.fetch_one(id=1)
    action = EbayItemAction(ebay_store=store)
    items = action.fetch_all_items()

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'scrapers', 'amzn'))

from amazonmws.model_managers import *

from atoe.actions import EbayStorePreferenceAction


if __name__ == "__main__":
    ebay_stores = EbayStoreModelManager.fetch()

    for ebay_store in ebay_stores:
        action = EbayStorePreferenceAction(ebay_store)
        action.set_user_pref()

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'scrapers', 'amzn'))

from amazonmws.model_managers import EbayStoreModelManager

from atoe.helpers import ListingHandler


if __name__ == "__main__":
    ebay_stores = EbayStoreModelManager.fetch()

    for ebay_store in ebay_stores:
        handler = ListingHandler(ebay_store)
        handler.run()

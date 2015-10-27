import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from amazonmws.ebaystore.listing import ListingHandler
from amazonmws.models import StormStore, EbayStore


if __name__ == "__main__":
    ebay_stores = StormStore.find(EbayStore, EbayStore.id == 1)

    if ebay_stores.count() > 0:
        for ebay_store in ebay_stores:
            handler = ListingHandler(ebay_store)
            handler.run()

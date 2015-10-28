import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from amazonmws import settings, utils
from amazonmws.ebaystore.listing import ListingHandler
from amazonmws.models import StormStore, EbayStore

import csv


if __name__ == "__main__":
    
    asins_exclude = None

    with open(os.path.join(settings.ROOT_PATH, 'tmp', 'EBAYListing.csv'), 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            try:
                item = StormStore.find(EbayItem, EbayItem.ebay_store_id == 3, EbayItem.asin == utils.str_to_unicode(row[0]).strip()).one()
                if item:
                    asins_exclude.append(item.ebid)
                else:
                    continue
            except StormError:
                continue

    ebay_stores = StormStore.find(EbayStore, EbayStore.id == 3)

    if ebay_stores.count() > 0:
        for ebay_store in ebay_stores:
            handler = ListingHandler(ebay_store, max_num_listing=900, asins_exclude=asins_exclude)
            handler.run()

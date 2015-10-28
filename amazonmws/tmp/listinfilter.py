import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

import csv

from storm.exceptions import StormError

from amazonmws import utils
from amazonmws.models import StormStore, AmazonItem, AmazonItemPicture, Scraper, EbayItem, Task, ItemQuantityHistory, EbayStore, LookupAmazonItem, Lookup, LookupOwnership

with open('EBAYListing.csv', 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
        try:
            item = StormStore.find(EbayItem, EbayItem.ebay_store_id == 3, EbayItem.asin == utils.str_to_unicode(row[0]).strip()).one()
            if item:
                print item.ebid
            else:
                continue
        except StormError:
            continue

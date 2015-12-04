import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import datetime

from storm.expr import Select, And, Desc, Not, SQLRaw
from storm.exceptions import StormError

from amazonmws import settings
from amazonmws.models import StormStore, EbayStore, EbayItem, zzAmazonItem as AmazonItem, zzAmazonItemPicture as AmazonItemPicture, zzAtoECategoryMap as AtoECategoryMap, zzAmazonItemOffer as AmazonItemOffer, zzAmazonBestsellers as AmazonBestsellers,zzEbayStorePreferredCategory as EbayStorePreferredCategory, zzExclBrand as ExclBrand
from amazonmws.loggers import GrayLogger as logger


def fetch_sold_for_listing():
    """fetch amazon items which sold by sellers in system - order by num of sold
    """
    query = 'select am.*, count(*) as count from transactions t left join ebay_items eb on t.item_id = eb.ebid left join zz__amazon_items am on eb.asin = am.asin where am.asin is not null group by eb.asin order by count;'

    results = StormStore.execute(Select(SQLRaw(query)))

    print results

    for result as results:
    	print "asin: " + str(result.asin) + " --- count: " + str(result.count)

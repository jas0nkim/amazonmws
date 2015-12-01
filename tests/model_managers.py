import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from amazonmws.model_managers import *

ebay_store = EbayStoreModelManager.fetch_one(id=2)
pref_cats = EbayStorePreferredCategoryModelManager.fetch(ebay_store=ebay_store)

count = 0;
exclude_asins = []
for pref_cat in pref_cats:
    items = AmazonItemModelManager.fetch_filtered_for_listing(pref_cat, 10, 
        asins_exclude=exclude_asins,
        listing_min_dollar=ebay_store.listing_min_dollar,
        listing_max_dollar=ebay_store.listing_max_dollar)
    for amazon_item, ebay_item in items:
        exclude_asins.append(amazon_item.asin)
        print amazon_item.asin + ' : ' + amazon_item.title 
        count += 1
print 'total: ' + str(count)    

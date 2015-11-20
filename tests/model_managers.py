import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from amazonmws.model_managers import *

ebay_store = EbayStoreModelManager.fetch_one(id=2)
pref_cats = EbayStorePreferredCategoryModelManager.fetch(ebay_store=ebay_store)

for pref_cat in pref_cats:
    if pref_cat.id == 10:
        items = AmazonItemModelManager.fetch_filtered_for_listing(pref_cat, 10)
        print items
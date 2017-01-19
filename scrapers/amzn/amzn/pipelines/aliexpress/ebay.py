import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..', 'rfi'))

import re
import RAKE

from django.core.exceptions import MultipleObjectsReturned

from amazonmws import settings as amazonmws_settings, utils as amazonmws_utils
from amazonmws.model_managers import *

from atoe.helpers import CategoryHandler, ListingHandler

from amzn.spiders import *
from amzn.items import AliexpressItem

# from rfi_listings.models import EbayItem


class AliexpressToEbayCategoryMapPipeline(object):
    """AliexpressItem only pipeline
    """
    
    def process_item(self, item, spider):
        if isinstance(item, AliexpressItem): # AliexpressItem (scrapy item)
            alx_category_breadcrumb = item['_category_route'].get('category', None)

            if not alx_category_breadcrumb:
                return item

            alx_to_e_map = AlxToEbayCategoryMapModelManager.fetch_one(aliexpress_category=alx_category_breadcrumb)
            if alx_to_e_map: # given aliexpress cagetory already exists in map table. skip it
                return item

            _rand_ebay_store = EbayStoreModelManager.fetch_one(random=True)
            handler = CategoryHandler(ebay_store=_rand_ebay_store)
            ebay_category_id, ebay_category_name = handler.find_ebay_category(alx_category_breadcrumb)
            AlxToEbayCategoryMapModelManager.create(aliexpress_category=alx_category_breadcrumb,
                ebay_category_id=ebay_category_id,
                ebay_category_name=ebay_category_name)
            category_features = handler.find_ebay_category_features(category_id=ebay_category_id)
            if category_features:
                ecf = EbayCategoryFeaturesModelManager.fetch_one(ebay_category_id=ebay_category_id)
                if ecf:
                    EbayCategoryFeaturesModelManager.update(feature=ecf,
                        upc_enabled=category_features.get('UPCEnabled', False),
                        variations_enabled=amazonmws_utils.convertEbayApiBooleanValue(category_features.get('VariationsEnabled', False)))
                else:
                    EbayCategoryFeaturesModelManager.create(ebay_category_id=ebay_category_id,
                        ebay_category_name=ebay_category_name,
                        upc_enabled=category_features.get('UPCEnabled', False),
                        variations_enabled=amazonmws_utils.convertEbayApiBooleanValue(category_features.get('VariationsEnabled', False)))
        return item

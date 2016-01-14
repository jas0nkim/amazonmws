import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'scrapers', 'amzn'))

import re

from amazonmws import settings as amazonmws_settings, utils as amazonmws_utils
from amazonmws.loggers import GrayLogger as logger
from amazonmws.model_managers import *

from atoe.actions import EbayItemAction


if __name__ == "__main__":
    store = EbayStoreModelManager.fetch_one(id=1)
    action = EbayItemAction(ebay_store=store)

    cmap = AtoECategoryMapModelManager.fetch(ebay_category_id=None)
    
    for c in cmap:
        try:
            trimmed_keywords = re.sub(r'([^\s\w]|_)+', ' ', c.amazon_category).strip()
            category_info = action.find_category(trimmed_keywords)

            AtoECategoryMapModelManager.update(c, ebay_category_id=category_info[0], ebay_category_name=category_info[1])
        except Exception:
            continue


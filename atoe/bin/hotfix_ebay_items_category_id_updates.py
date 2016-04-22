import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'scrapers', 'amzn'))

from amazonmws import django_cli
django_cli.execute()

from amazonmws import settings as amazonmws_settings, utils as amazonmws_utils
from amazonmws.loggers import GrayLogger as logger
from amazonmws.model_managers import *

from atoe.actions import EbayItemAction


def _revise_item_category(ebay_store, ebay_item):
    amazon_item = AmazonItemModelManager.fetch_one(ebay_item.asin)
    if not amazon_item:
        return False

    atoe_map = AtoECategoryMapModelManager.fetch_one(amazon_category=amazon_item.category)
    if not atoe_map:
        return False

    # compare with category map table, and only perform revise item category if they are not the same
    if ebay_item.ebay_category_id == atoe_map.ebay_category_id:
        return False

    action = EbayItemAction(ebay_store=ebay_store, ebay_item=ebay_item, amazon_item=amazon_item)
    action.revise_item_category(category_id=atoe_map.ebay_category_id)
    # update database entry
    EbayItemModelManager.update_category(ebay_item=ebay_item, ebay_category_id=atoe_map.ebay_category_id)
    return True


if __name__ == "__main__":
    store = EbayStoreModelManager.fetch_one(id=1)
    ebay_items = EbayItemModelManager.fetch(ebay_store_id=store.id, created_at__gt='2016-04-20 00:00:00')

    for ebay_item in ebay_items:
        _revise_item_category(ebay_store=store, ebay_item=ebay_item)

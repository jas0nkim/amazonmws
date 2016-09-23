import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'scrapers', 'amzn'))

from amazonmws import django_cli
django_cli.execute()

from amazonmws import settings as amazonmws_settings, utils as amazonmws_utils
from amazonmws.loggers import GrayLogger as logger
from amazonmws.model_managers import *

from atoe.actions import EbayItemAction


def _revise_item_title_and_description(ebay_store, ebay_item, description_only=False):
    amazon_item = AmazonItemModelManager.fetch_one(ebay_item.asin)
    if not amazon_item:
        return False

    action = EbayItemAction(ebay_store=ebay_store, ebay_item=ebay_item, amazon_item=amazon_item)
    if not description_only:
        action.revise_item(title=amazon_item.title)
    else:
        action.revise_item_description()
    return True


if __name__ == "__main__":
    store = EbayStoreModelManager.fetch_one(id=1)
    ebay_items = EbayItemModelManager.fetch(ebay_store_id=store.id)

    for ebay_item in ebay_items:
        _revise_item_title_and_description(ebay_store=store, ebay_item=ebay_item, description_only=True)
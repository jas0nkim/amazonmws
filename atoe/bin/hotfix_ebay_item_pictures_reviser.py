import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'scrapers', 'amzn'))

from amazonmws import django_cli
django_cli.execute()

from amazonmws import settings as amazonmws_settings, utils as amazonmws_utils
from amazonmws.loggers import GrayLogger as logger
from amazonmws.model_managers import *

from atoe.helpers import ListingHandler


def run():
    _ebay_item_id = '281946491714'

    ebay_item = EbayItemModelManager.fetch_one(ebid=_ebay_item_id)

    if not ebay_item:
        return False

    handler = ListingHandler(ebay_store=ebay_item.ebay_store)
    revised_pictures = AmazonItemPictureModelManager.fetch(asin=ebay_item.asin)
    if revised_pictures.count() < 1:
        return False
    handler.revise_item(ebay_item=ebay_item, pictures=revised_pictures)


if __name__ == "__main__":
    run()

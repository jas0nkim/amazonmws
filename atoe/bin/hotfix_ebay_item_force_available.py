import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'scrapers', 'amzn'))

from amazonmws import django_cli
django_cli.execute()

from amazonmws import settings as amazonmws_settings, utils as amazonmws_utils
from amazonmws.loggers import GrayLogger as logger
from amazonmws.model_managers import *

from atoe.actions import EbayItemAction


def run():
    _ebay_item_id = '281946848183'

    ebay_item = EbayItemModelManager.fetch_one(ebid=_ebay_item_id)

    if not ebay_item:
        return False

    action = EbayItemAction(ebay_store=ebay_item.ebay_store, ebay_item=ebay_item)
    action.revise_inventory(eb_price=None, quantity=1)


if __name__ == "__main__":
    run()

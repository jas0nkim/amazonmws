import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

import datetime
import uuid
import json

from amazonmws import settings, utils
from amazonmws.loggers import GrayLogger as logger, StaticFieldFilter, get_logger_name

def generate_revise_inventory_status_obj(ebay_item, price=None, quantity=None):
    if price == None and quantity == None:
        return None

    item = settings.EBAY_REVISE_INVENTORY_STATUS_TEMPLATE
    item['MessageID'] = uuid.uuid4()
    item['InventoryStatus']['ItemID'] = ebay_item.ebid
    
    if quantity != None:
        item['InventoryStatus']['Quantity'] = quantity
    else:
        item['InventoryStatus'].pop("Quantity", None)

    if price != None:
        item['InventoryStatus']['StartPrice'] = price
    else:
        item['InventoryStatus'].pop("StartPrice", None)

    return item

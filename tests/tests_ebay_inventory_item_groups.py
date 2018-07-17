import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'rfi'))

###### setting django module ######

os.environ['DJANGO_SETTINGS_MODULE'] = 'rfi.settings'

import django
django.setup()

###################################

from amazonmws.model_managers import *
from atoe.actions import EbayInventoryItemGroupAction


def _test_create_inventory_item_groups(ebay_store):
    action = EbayInventoryItemGroupAction(ebay_store=ebay_store)
    payload = {
        "aspects": {
            "Brand": ["TextMate"]
        },
        "title": "iDOO Matte Rubber Coated Soft Touch Plastic Hard Case for MacBook Air 13 inch...",
        "description": "Men's solid polo shirts in five colors (Green, Blue, Red, Black, and White), and sizes ranges from small to XL.",
        "imageUrls": [
            "https://i.ebayimg.com/00/s/MTUwMFgxNTAw/z/0OoAAOSwCTBbR9Dd/$_1.JPG"
        ],
        "variantSKUs": [
            "834753465324",
            "834753465325"
        ],
        "variesBy": { 
            "aspectsImageVariesBy": [
                "Color"
            ],
            "specifications": [
                { 
                    "name": "Color",
                    "values": [
                        "Black",
                        "Red"
                    ]
                }
            ]
        }
    }
    result = action.create_or_update_inventory_item_group(inventory_item_group_key='12345678', https_payload=payload)
    print("result: " + str(result))


if __name__ == "__main__":
    ebay_store = EbayStoreModelManager.fetch_one(id=1)
    _test_create_inventory_item_groups(ebay_store=ebay_store)

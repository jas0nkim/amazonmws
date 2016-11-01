import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))

import getopt
import uuid

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging

from amazonmws import django_cli
django_cli.execute()

from amazonmws import utils as amazonmws_utils
from amazonmws.loggers import set_root_graylogger, GrayLogger as logger
from amazonmws.model_managers import *

from atoe.helpers import ListingHandler, CategoryHandler
from atoe.actions import EbayItemAction

__target_amazon_categories = ["Clothing, Shoes & Jewelry : Women",]
__ebay_store_id = 1


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "h")
    except getopt.GetoptError:
        print 'hotfix_wrong_ebay_category.py'
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print 'hotfix_wrong_ebay_category.py'
            sys.exit()
    run()


def run():
    # 1. create/update a_to_e_category_maps table (correction)
    # 2. find all asins from amazon_items with __target_amazon_categories
    # 3. update ebay items of asins

    ebay_store_id = __ebay_store_id
    # create/update a_to_e_category_maps table (correction)
    ate_map = update_and_get_ate_category_maps(ebay_store_id, __target_amazon_categories)

    # - find all asins from amazon_items with __target_amazon_categories
    # - update ebay items of asins
    update_ebay_items(ebay_store_id, ate_map)


def update_and_get_ate_category_maps(ebay_store_id, amazon_categories):
    ate_map = {}
    ebay_store = EbayStoreModelManager.fetch_one(id=ebay_store_id)
    handler = CategoryHandler(ebay_store=ebay_store)
    for amazon_category_breadcrumb in amazon_categories:
        a_to_b_maps = AtoECategoryMapModelManager.fetch(amazon_category__icontains=amazon_category_breadcrumb)
        print("*** NUM OF MAPS {} ***".format(a_to_b_maps.count()))
        for a_to_b_map in a_to_b_maps:
            print("*** EXISTING AMAZON CATEGORY - EBAY CATEGORY: {} <===> {} ***".format(a_to_b_map.amazon_category, a_to_b_map.ebay_category_name))            
            old_ebay_category_id = a_to_b_map.ebay_category_id
            ebay_category_id, ebay_category_name = handler.find_ebay_category(a_to_b_map.amazon_category)
            if str(ebay_category_id) != str(old_ebay_category_id):
                AtoECategoryMapModelManager.update(a_to_b_map,
                    ebay_category_id=ebay_category_id,
                    ebay_category_name=ebay_category_name)
                ate_map[a_to_b_map.amazon_category] = ebay_category_id
                print("*** EBAY CATEORY ID UPDATED TO: {} ***".format(ebay_category_name))
    return ate_map

def update_ebay_items(ebay_store_id, ate_map):
    ebay_store = EbayStoreModelManager.fetch_one(id=ebay_store_id)
    for amazon_category_breadcrumb, new_ebay_category_id in ate_map.iteritems():
        a_items = AmazonItemModelManager.fetch(category=amazon_category_breadcrumb)
        for amazon_item in a_items:
            try:
                ebay_item = EbayItemModelManager.fetch_one(ebay_store_id=ebay_store_id, asin=amazon_item.parent_asin)
                if not ebay_item:
                    continue
                if str(ebay_item.ebay_category_id) != str(new_ebay_category_id):
                    action = EbayItemAction(ebay_store=ebay_store, ebay_item=ebay_item, amazon_item=amazon_item)
                    success = action.revise_item_category(category_id=str(new_ebay_category_id))
                    if success:
                        # update database entry
                        EbayItemModelManager.update_category(ebay_item=ebay_item, ebay_category_id=str(new_ebay_category_id))
                        print("*** [EBID:{}] CATEORY ID UPDATED : {} -> {} ***".format(ebay_item.ebid, ebay_item.ebay_category_id, new_ebay_category_id))
            except:
                e = sys.exc_info()[0]
                logger.exception(e)
                continue


if __name__ == "__main__":
    main(sys.argv[1:])

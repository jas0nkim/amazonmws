import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))

import re
import RAKE

from amazonmws import settings as amazonmws_settings

from amzn.spiders.amazon_pricewatch import AmazonPricewatchSpider
from amzn.items import AmazonItem as AmazonScrapyItem

from atoe.actions import EbayItemAction
from atoe.models import AtoECategoryMapModelManager


class AtoECategoryMappingPipeline(object):
    def process_item(self, item, spider):
        if isinstance(spider, AmazonPricewatchSpider):
            return item

        if isinstance(item, AmazonScrapyItem): # AmazonItem (scrapy item)
            if item.get('category', None) != None:
                a_to_b_map = AtoECategoryMapModelManager.fetch_one(item.get('category'))
                if a_to_b_map == None:
                    ebay_category_id, ebay_category_name = self.__find_eb_cat_by_am_cat(item)
                    AtoECategoryMapModelManager.create(item.get('category'), ebay_category_id=ebay_category_id, ebay_category_name=ebay_category_name)
        return item

    def __find_eb_cat_by_am_cat(self, item):
        Rake = RAKE.Rake(os.path.join(amazonmws_settings.APP_PATH, 'rake', 'stoplists', 'SmartStoplist.txt'));
        category_route = [re.sub(r'([^\s\w]|_)+', ' ', c).strip() for c in item.get('category').split(':')]
        depth = len(category_route)
        while True:
            keywords = Rake.run(' '.join(category_route));
            if len(keywords) > 0:
                ebay_action = EbayItemAction()
                ebay_category_info = ebay_action.find_category(keywords[0][0])
                if not ebay_category_info and depth >= 4:
                    category_route = category_route[:-1]
                    depth -= 1
                else:
                    return ebay_category_info
            else:
                break
        return (None, None)

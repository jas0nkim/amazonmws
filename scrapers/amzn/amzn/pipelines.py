import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

import re
import datetime
from decimal import Decimal

from scrapy.exceptions import DropItem
from storm.exceptions import StormError

import RAKE

from amazonmws import settings as amazon_settings, utils as amazon_utils
from amazonmws.models import StormStore, zzAmazonItem, zzAmazonItemPicture, zzAtoECategoryMap, zzAmazonBestsellers, zzAmazonBestsellersArchived
from amzn.items import AmazonItem, AmazonPictureItem, AmazonBestsellerItem


class AmazonItemDBStoragePipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, AmazonItem): # AmazonItem
            self.__store_amazon_item(item)
        elif isinstance(item, AmazonPictureItem): # AmazonPictureItem
            self.__store_amazon_picture_item(item)
        elif isinstance(item, AmazonBestsellerItem): # AmazonBestsellerItem
            self.__store_amazon_bestseller_item(item)
        else:
            raise DropItem
        return item

    def __store_amazon_item(self, item):
        a_item = None
        try:
            a_item = StormStore.find(zzAmazonItem, zzAmazonItem.asin == item.get('asin', '')).one()
        except StormError, e:
            a_item = None
        
        try:
            if a_item == None:
                a_item = zzAmazonItem()
                a_item.asin = item.get('asin')
                a_item.url = item.get('url')
                a_item.category = item.get('category')
                a_item.created_at = datetime.datetime.now()

            if item.get('status', True) == True:
                a_item.title = item.get('title')
                a_item.price = Decimal(item.get('price')).quantize(Decimal('1.00'))
                a_item.quantity = item.get('quantity')
                a_item.features = item.get('features')
                a_item.description = item.get('description')
                a_item.review_count = item.get('review_count')
                a_item.avg_rating = item.get('avg_rating')
                a_item.is_fba = item.get('is_fba')
                a_item.is_fba_by_other_seller = item.get('is_fba_by_other_seller')
                a_item.is_addon = item.get('is_addon')
            
            # if status == False, just update status field.
            a_item.status = item.get('status')
            a_item.updated_at = datetime.datetime.now()

            StormStore.add(a_item)
            StormStore.commit()
        except StormError, e:
            StormStore.rollback()
        return a_item

    def __store_amazon_picture_item(self, item):
        a_item_pic = None
        try:
            a_item_pic = StormStore.find(zzAmazonItemPicture, 
                zzAmazonItemPicture.asin == item.get('asin'),
                zzAmazonItemPicture.picture_url == item.get('picture_url')).one()
        except StormError, e:
            a_item_pic = None

        if a_item_pic != None: # already exists. do nothing
            return item
        
        try:
            a_item_pic = zzAmazonItemPicture()
            a_item_pic.asin = item.get('asin')
            a_item_pic.picture_url = item.get('picture_url')
            a_item_pic.created_at = datetime.datetime.now()
            a_item_pic.updated_at = datetime.datetime.now()

            StormStore.add(a_item_pic)
            StormStore.commit()
        except StormError, e:
            StormStore.rollback()
        return a_item_pic

    def __store_amazon_bestseller_item(self, item):
        a_bs = None
        try:
            a_bs = StormStore.find(zzAmazonBestsellers, 
                zzAmazonBestsellers.asin == item.get('asin'),
                zzAmazonBestsellers.bestseller_category == item.get('bestseller_category')).one()
        except StormError, e:
            a_bs = None

        try:
            if a_bs == None:
                a_bs = zzAmazonBestsellers()
                a_bs.asin = item.get('asin')
                a_bs.bestseller_category = item.get('bestseller_category')
                a_bs.created_at = datetime.datetime.now()
            
            a_bs.rank = item.get('rank')
            a_bs.updated_at = datetime.datetime.now()

            StormStore.add(a_bs)
            StormStore.commit()
        except StormError, e:
            StormStore.rollback()
        return a_bs


class AtoECategoryMappingPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, AmazonItem): # AmazonItem
            if item.get('category', None) != None:
                try:
                    a_to_b_map = StormStore.find(zzAtoECategoryMap, 
                        zzAtoECategoryMap.amazon_category == item.get('category')).one()
                except StormError, e:
                    a_to_b_map = None

                if a_to_b_map == None:
                    ebay_category_info = self.__find_eb_cat_by_am_cat(item)
                    if ebay_category_info != None:
                        self.__store_a_to_b_category_map(item, ebay_category_info)
        return item

    def __find_eb_cat_by_am_cat(self, item):
        Rake = RAKE.Rake(os.path.join(amazon_settings.APP_PATH, 'rake', 'stoplists', 'SmartStoplist.txt'));
        category_route = [re.sub(r'([^\s\w]|_)+', ' ', c).strip() for c in item.get('category').split(':')]
        depth = len(category_route)
        while True:
            keywords = Rake.run(' '.join(category_route));
            if len(keywords) > 0:
                ebay_category_info = amazon_utils.find_ebay_category_info(keywords[0][0], item.get('asin'))
                if not ebay_category_info and depth >= 4:
                    category_route = category_route[:-1]
                    depth -= 1
                else:
                    return ebay_category_info
            else:
                break
        return None

    def __store_a_to_b_category_map(self, item, ebay_category_info):
        try:
            a_to_b_map = zzAtoECategoryMap()
            a_to_b_map.amazon_category = item.get('category')
            a_to_b_map.ebay_category_id = unicode(ebay_category_info[0])
            a_to_b_map.ebay_category_name = unicode(ebay_category_info[1])
            a_to_b_map.created_at = datetime.datetime.now()
            a_to_b_map.updated_at = datetime.datetime.now()

            StormStore.add(a_to_b_map)
            StormStore.commit()
        except StormError, e:
            StormStore.rollback()
        return a_to_b_map


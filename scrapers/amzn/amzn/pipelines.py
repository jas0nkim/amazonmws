import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

import datetime
from decimal import Decimal

from scrapy.exceptions import DropItem
from storm.exceptions import StormError

from amazonmws.models import StormStore, zzAmazonItem, zzAmazonItemPicture
from amzn.items import AmazonItem, AmazonPictureItem


class AmazonPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, AmazonItem): # AmazonItem
            a_item = None
            try:
                a_item = StormStore.find(zzAmazonItem, zzAmazonItem.asin == item.get('asin')).one()
            except StormError, e:
                a_item = None

            if a_item == None:
                a_item = zzAmazonItem()
                a_item.asin = item.get('asin')
                a_item.url = item.get('url')
                a_item.category = item.get('category')

            try:
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
                a_item.created_at = datetime.datetime.now()
                a_item.updated_at = datetime.datetime.now()

                StormStore.add(a_item)
                StormStore.commit()
            except StormError, e:
                StormStore.rollback()

        elif isinstance(item, AmazonPictureItem): # AmazonPictureItem
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
        
        else:
            raise DropItem
        
        return item


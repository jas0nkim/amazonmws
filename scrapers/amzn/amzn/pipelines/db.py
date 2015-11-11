import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))

import datetime

from scrapy.exceptions import DropItem

from storm.exceptions import StormError

from amazonmws import utils as amazonmws_utils
from amazonmws.models import StormStore, zzAmazonItem as AmazonItem, zzAmazonItemPicture as AmazonItemPicture, zzAtoECategoryMap as AtoECategoryMap, zzAmazonBestsellers as AmazonBestsellers, zzAmazonBestsellersArchived as AmazonBestsellersArchived, zzAmazonItemOffer as AmazonItemOffer

from amzn.items import AmazonItem as AmazonScrapyItem, AmazonPictureItem as AmazonPictureScrapyItem, AmazonBestsellerItem as AmazonBestsellerScrapyItem, AmazonOfferItem as AmazonOfferScrapyItem


class AmazonItemDBPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, AmazonScrapyItem): # AmazonItem (scrapy item)
            self.__store_amazon_item(item)
        elif isinstance(item, AmazonPictureScrapyItem): # AmazonPictureItem (scrapy item)
            self.__store_amazon_picture_item(item)
        elif isinstance(item, AmazonBestsellerScrapyItem): # AmazonBestsellerItem (scrapy item)
            self.__store_amazon_bestseller_item(item)
        elif isinstance(item, AmazonOfferScrapyItem): # AmazonOfferItem (scrapy item)
            self.__store_amazon_offer_item(item)
        else:
            raise DropItem
        return item

    def __store_amazon_item(self, item):
        a_item = None
        try:
            a_item = StormStore.find(AmazonItem, AmazonItem.asin == item.get('asin', '')).one()
        except StormError, e:
            a_item = None
        
        try:
            if a_item == None:
                a_item = AmazonItem()
                a_item.asin = item.get('asin')
                a_item.url = item.get('url')
                a_item.category = item.get('category')
                a_item.created_at = datetime.datetime.now()

            if item.get('status', True) == True:
                a_item.title = item.get('title')
                a_item.price = amazonmws_utils.number_to_dcmlprice(item.get('price'))
                a_item.market_price = amazonmws_utils.number_to_dcmlprice(item.get('market_price'))
                a_item.quantity = item.get('quantity')
                a_item.features = item.get('features')
                a_item.description = item.get('description')
                a_item.review_count = item.get('review_count')
                a_item.avg_rating = item.get('avg_rating')
                a_item.is_fba = item.get('is_fba')
                a_item.is_addon = item.get('is_addon')
                a_item.merchant_id = item.get('merchant_id')
                a_item.merchant_name = item.get('merchant_name')
            
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
            a_item_pic = StormStore.find(AmazonItemPicture, 
                AmazonItemPicture.asin == item.get('asin'),
                AmazonItemPicture.picture_url == item.get('picture_url')).one()
        except StormError, e:
            a_item_pic = None

        if a_item_pic != None: # already exists. do nothing
            return item
        
        try:
            a_item_pic = AmazonItemPicture()
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
            a_bs = StormStore.find(AmazonBestsellers, 
                AmazonBestsellers.bestseller_category == item.get('bestseller_category'),
                AmazonBestsellers.rank == item.get('rank')).one()
        except StormError, e:
            a_bs = None

        try:
            if a_bs == None:
                a_bs = AmazonBestsellers()
                a_bs.bestseller_category = item.get('bestseller_category')
                a_bs.rank = item.get('rank')
                a_bs.created_at = datetime.datetime.now()
            
            a_bs.url = item.get('url')
            a_bs.asin = item.get('asin')
            a_bs.updated_at = datetime.datetime.now()

            StormStore.add(a_bs)
            StormStore.commit()
        except StormError, e:
            StormStore.rollback()
        return a_bs

    def __store_amazon_offer_item(self, item):
        a_offer = None
        try:
            a_offer = StormStore.find(AmazonItemOffer,
                AmazonItemOffer.asin == item.get('asin'),
                AmazonItemOffer.is_fba == item.get('is_fba'),
                AmazonItemOffer.merchant_id == item.get('merchant_id'),
                AmazonItemOffer.merchant_name == item.get('merchant_name')).one()
        except StormError, e:
            a_offer = None

        try:
            if a_offer == None:
                a_offer = AmazonItemOffer()
                a_offer.asin = item.get('asin')
                a_offer.is_fba = item.get('is_fba')
                a_offer.merchant_id = item.get('merchant_id')
                a_offer.merchant_name = item.get('merchant_name')
                a_offer.created_at = datetime.datetime.now()
            
            a_offer.price = amazonmws_utils.number_to_dcmlprice(item.get('price'))
            a_offer.quantity = item.get('quantity')
            a_offer.revision = item.get('revision')
            a_offer.updated_at = datetime.datetime.now()

            StormStore.add(a_offer)
            StormStore.commit()
        except StormError, e:
            StormStore.rollback()
        return a_offer

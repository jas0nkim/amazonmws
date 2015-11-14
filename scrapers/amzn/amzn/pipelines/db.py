import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))

import datetime

from scrapy.exceptions import DropItem

from amazonmws import utils as amazonmws_utils
from amazonmws.model_managers.amazon_items import *

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
        amazon_item = AmazonItemModelManager.fetch_one(item.get('asin', ''))
        if amazon_item == None and not item.get('status'): # do nothing
            return

        if amazon_item == None: # create item
            AmazonItemModelManager.create(asin=item.get('asin'),
                url=item.get('url'),
                category=item.get('category'),
                title=item.get('title'),
                price=amazonmws_utils.number_to_dcmlprice(item.get('price')),
                market_price=amazonmws_utils.number_to_dcmlprice(item.get('market_price')),
                quantity=item.get('quantity'),
                features=item.get('features'),
                description=item.get('description'),
                review_count=item.get('review_count'),
                avg_rating=item.get('avg_rating'),
                is_fba=item.get('is_fba'),
                is_addon=item.get('is_addon'),
                merchant_id=item.get('merchant_id'),
                merchant_name=item.get('merchant_name'),
                brand_name=item.get('brand_name'),
                status=item.get('status'))
        else: # update item
            if not item.get('status'):
                AmazonItemModelManager.inactive(amazon_item)
                return
            
            AmazonItemModelManager.update(amazon_item,
                url=item.get('url'),
                category=item.get('category'),
                title=item.get('title'),
                price=amazonmws_utils.number_to_dcmlprice(item.get('price')),
                market_price=amazonmws_utils.number_to_dcmlprice(item.get('market_price')),
                quantity=item.get('quantity'),
                features=item.get('features'),
                description=item.get('description'),
                review_count=item.get('review_count'),
                avg_rating=item.get('avg_rating'),
                is_fba=item.get('is_fba'),
                is_addon=item.get('is_addon'),
                merchant_id=item.get('merchant_id'),
                merchant_name=item.get('merchant_name'),
                brand_name=item.get('brand_name'),
                status=item.get('status'))
        return True

    def __store_amazon_picture_item(self, item):
        picture = AmazonItemPictureModelManager.fetch_one(item.get('asin'), item.get('picture_url'))
        if not picture: # create
            AmazonItemPictureModelManager.create(asin=item.get('asin'),
                picture_url=item.get('picture_url'))
        return True

    def __store_amazon_bestseller_item(self, item):
        bs = AmazonBestsellersModelManager.fetch_one(item.get('bestseller_category_url'),
                item.get('rank'))
        if not bs:
            AmazonBestsellersModelManager.create(asin=item.get('asin'),
                bestseller_category=item.get('bestseller_category'),
                bestseller_category_url=item.get('bestseller_category_url'),
                rank=item.get('rank'))
        else:
            AmazonBestsellersModelManager.update(bs,
                asin=item.get('asin'),
                bestseller_category=item.get('bestseller_category'))
        return True

    def __store_amazon_offer_item(self, item):
        offer = AmazonItemOfferModelManager.fetch_one(item.get('asin'),
                    item.get('is_fba'),
                    item.get('merchant_id'),
                    item.get('merchant_name'))
        if not offer:
            AmazonItemOfferModelManager.create(asin=item.get('asin'),
                price=amazonmws_utils.number_to_dcmlprice(item.get('price')),
                quantity=item.get('quantity'),
                is_fba=item.get('is_fba'),
                merchant_id=item.get('merchant_id'),
                merchant_name=item.get('merchant_name'),
                revision=item.get('revision'))
        else:
            AmazonItemOfferModelManager.update(offer,
                price=amazonmws_utils.number_to_dcmlprice(item.get('price')),
                quantity=item.get('quantity'),
                revision=item.get('revision'))
        return True

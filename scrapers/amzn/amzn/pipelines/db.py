import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))

import datetime

from scrapy.exceptions import DropItem

from amazonmws import django_cli
django_cli.execute()

from amazonmws import utils as amazonmws_utils
from amazonmws.model_managers.amazon_items import *
from amazonmws.model_managers.ebay_stores import *

from amzn.items import AmazonItem as AmazonScrapyItem, AmazonPictureItem as AmazonPictureScrapyItem, AmazonBestsellerItem as AmazonBestsellerScrapyItem, AmazonOfferItem as AmazonOfferScrapyItem


class AmazonItemDBPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, AmazonScrapyItem): # AmazonItem (scrapy item)
            self.__store_amazon_item(item)
            if spider.task_id and spider.ebay_store_id:
                self.__store_amazon_scrape_tasks(task_id=spider.task_id, ebay_store_id=spider.ebay_store_id, item=item)
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
                specifications=item.get('specifications'),
                review_count=item.get('review_count'),
                avg_rating=item.get('avg_rating'),
                is_fba=item.get('is_fba'),
                is_addon=item.get('is_addon'),
                is_pantry=item.get('is_pantry'),
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
                specifications=item.get('specifications'),
                review_count=item.get('review_count'),
                avg_rating=item.get('avg_rating'),
                is_fba=item.get('is_fba'),
                is_addon=item.get('is_addon'),
                is_pantry=item.get('is_pantry'),
                merchant_id=item.get('merchant_id'),
                merchant_name=item.get('merchant_name'),
                brand_name=item.get('brand_name'),
                status=item.get('status'))
        return True

    def __store_amazon_picture_item(self, item):
        picture = AmazonItemPictureModelManager.fetch_one(item.get('asin'), item.get('picture_url'))
        if not picture: # create
            AmazonItemPictureModelManager.create(
                asin=item.get('asin'),
                picture_url=item.get('picture_url'))
        return True

    def __store_amazon_bestseller_item(self, item):
        bs = AmazonBestsellerModelManager.fetch_one(item.get('bestseller_category_url'),
                item.get('rank'))
        if not bs:
            AmazonBestsellerModelManager.create(
                asin=item.get('asin'),
                bestseller_category=item.get('bestseller_category'),
                bestseller_category_url=item.get('bestseller_category_url'),
                rank=item.get('rank'),
                avg_rating=item.get('avg_rating'),
                review_count=item.get('review_count'))
        else:
            AmazonBestsellerModelManager.update(bs,
                amazon_item__asin=item.get('asin'),
                bestseller_category=item.get('bestseller_category'),
                avg_rating=item.get('avg_rating'),
                review_count=item.get('review_count'))
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


    def __store_amazon_scrape_tasks(self, task_id, ebay_store_id, item):
        t = AmazonScrapeTaskModelManager.fetch_one(task_id=task_id, ebay_store_id=ebay_store_id, asin=item.get('asin'))
        if not t:
            AmazonScrapeTaskModelManager.create(
                task_id=task_id,
                ebay_store_id=ebay_store_id,
                asin=item.get('asin'))
        return True

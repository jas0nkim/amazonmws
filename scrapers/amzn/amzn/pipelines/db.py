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
            if self.__store_amazon_item(item, max_amazon_price=spider.max_amazon_price, min_amazon_price=spider.min_amazon_price):
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

    def __is_valid_item(self, item):
        # check if variation, and valid
        if item.get('variation_specifics', None):
            parent_asin = item.get('parent_asin') if item.get('parent_asin') else item.get('asin')
            asin = item.get('asin')
            if parent_asin == asin:
                # a variation cannot have same parent_asin and asin
                return False
        return True

    def __store_amazon_item(self, item, max_amazon_price=None, min_amazon_price=None):
        self.__handle_redirected_asin(redirected_asins=item.get('_redirected_asins', {}))

        amazon_item = AmazonItemModelManager.fetch_one(item.get('asin', ''))
        if amazon_item == None and not item.get('status'): # do nothing
            return False

        if not self.__is_valid_item(item):
            return False

        if max_amazon_price and amazonmws_utils.number_to_dcmlprice(item.get('price')) > max_amazon_price:
            return False

        if min_amazon_price and amazonmws_utils.number_to_dcmlprice(item.get('price')) < min_amazon_price:
            return False

        if amazon_item == None: # create item
            AmazonItemModelManager.create(asin=item.get('asin'),
                parent_asin=item.get('parent_asin') if item.get('parent_asin') else item.get('asin'),
                url=item.get('url'),
                category=item.get('category'),
                title=item.get('title'),
                price=amazonmws_utils.number_to_dcmlprice(item.get('price')),
                market_price=amazonmws_utils.number_to_dcmlprice(item.get('market_price')),
                quantity=item.get('quantity'),
                features=item.get('features'),
                description=item.get('description'),
                specifications=item.get('specifications'),
                variation_specifics=item.get('variation_specifics'),
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
                return False

            AmazonItemModelManager.update(amazon_item,
                parent_asin=item.get('parent_asin') if item.get('parent_asin') else item.get('asin'),
                url=item.get('url'),
                category=item.get('category'),
                title=item.get('title'),
                price=amazonmws_utils.number_to_dcmlprice(item.get('price')),
                market_price=amazonmws_utils.number_to_dcmlprice(item.get('market_price')),
                quantity=item.get('quantity'),
                features=item.get('features'),
                description=item.get('description'),
                specifications=item.get('specifications'),
                variation_specifics=item.get('variation_specifics'),
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
        picture_urls = item.get('picture_urls')
        if len(picture_urls) < 1:
            return False
        return AmazonItemPictureModelManager.save_item_pictures(asin=item.get('asin'), picture_urls=picture_urls)

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
                asin=item.get('asin'),
                parent_asin=item.get('parent_asin') if item.get('parent_asin') else item.get('asin'))
        return True

    def __handle_redirected_asin(self, redirected_asins):
        """ make OOS if any redrected asin (not the same as end-point/final asin)
        """
        if len(redirected_asins) > 0:
            for r_asin in redirected_asins.values():
                a_item = AmazonItemModelManager.fetch_one(r_asin)
                if not a_item:
                    continue
                AmazonItemModelManager.oos(item=a_item)

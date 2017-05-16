import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))

import datetime

from scrapy.exceptions import DropItem

from amazonmws import django_cli
django_cli.execute()

from amazonmws import utils as amazonmws_utils
from amazonmws.model_managers.amazon_items import *
from amazonmws.model_managers.ebay_stores import *

from amzn.spiders import *
from amzn.items import AmazonItem as AmazonScrapyItem, AmazonPictureItem as AmazonPictureScrapyItem, AmazonBestsellerItem as AmazonBestsellerScrapyItem, AmazonOfferItem as AmazonOfferScrapyItem, AmazonApparelItem as AmazonApparelScrapyItem


class AmazonItemCachePipeline(object):

    def __is_valid_item(self, item):
        # check if variation, and valid
        if item.get('variation_specifics', None):
            parent_asin = item.get('parent_asin') if item.get('parent_asin') else item.get('asin')
            asin = item.get('asin')
            if parent_asin == asin:
                # a variation cannot have same parent_asin and asin
                return False
        return True

    def __handle_redirected_asins(self, redirected_asins):
        """ make OOS if any redrected asin (not the same as end-point/final asin)
        """
        if len(redirected_asins) > 0:
            for r_asin in redirected_asins.values():
                a_item = AmazonItemModelManager.fetch_one(asin=r_asin)
                if not a_item:
                    continue
                AmazonItemModelManager.oos(item=a_item)

    def __cache_amazon_item(self, item, spider):
        self.__handle_redirected_asins(redirected_asins=item.get('_redirected_asins', {}))

        amazon_item = AmazonItemModelManager.fetch_one(asin=item.get('asin', ''))
        if amazon_item == None: # create item
            if not item.get('status'): # do nothing
                # do not create new entry for any invalid data (i.e. 404 pages)
                return False
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
                has_sizechart=item.get('has_sizechart'),
                international_shipping=True if hasattr(spider, 'international_shipping') and spider.international_shipping == True else False,
                merchant_id=item.get('merchant_id'),
                merchant_name=item.get('merchant_name'),
                brand_name=item.get('brand_name'),
                meta_title=item.get('meta_title'),
                meta_description=item.get('meta_description'),
                meta_keywords=item.get('meta_keywords'),
                status=item.get('status'))
        else: # update item
            if not item.get('status'):
                AmazonItemModelManager.inactive(amazon_item)
                return True
            AmazonItemModelManager.update(amazon_item,
                parent_asin=item.get('parent_asin') if item.get('parent_asin', None) else item.get('asin'),
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
                has_sizechart=item.get('has_sizechart'),
                international_shipping=True if hasattr(spider, 'international_shipping') and spider.international_shipping == True else amazon_item.international_shipping,
                merchant_id=item.get('merchant_id'),
                merchant_name=item.get('merchant_name'),
                brand_name=item.get('brand_name'),
                meta_title=item.get('meta_title'),
                meta_description=item.get('meta_description'),
                meta_keywords=item.get('meta_keywords'),
                status=item.get('status'))
        return True

    def __cache_amazon_picture_item(self, item):
        picture_urls = item.get('picture_urls')
        if len(picture_urls) < 1:
            return False
        return AmazonItemPictureModelManager.save_item_pictures(asin=item.get('asin'), picture_urls=picture_urls)

    def process_item(self, item, spider):
        if isinstance(item, AmazonScrapyItem): # AmazonItem (scrapy item)
            if item.get('_cached', False):
                logger.info("[ASIN:{}] _cached - no database saving".format(item.get('asin')))
                # this item is cached. do not save into db
                return item
            if not self.__is_valid_item(item):
                item['status'] = False
            self.__cache_amazon_item(item, spider)
        elif isinstance(item, AmazonPictureScrapyItem): # AmazonPictureItem (scrapy item)
            self.__cache_amazon_picture_item(item)
        return item


class ScrapyTaskPipeline(object):

    def __handle_redirected_asins(self, redirected_asins, task_id, ebay_store_id):
        """ make OOS if any redrected asin (not the same as end-point/final asin)
        """
        if len(redirected_asins) > 0:
            for r_asin in redirected_asins.values():
                a_item = AmazonItemModelManager.fetch_one(asin=r_asin)
                if not a_item:
                    continue
                self.__store_amazon_scrape_tasks(task_id=task_id,
                    ebay_store_id=ebay_store_id,
                    asin=a_item.asin,
                    parent_asin=a_item.parent_asin)

    def __store_amazon_scrape_tasks(self, task_id, ebay_store_id, asin, parent_asin):
        t = AmazonScrapeTaskModelManager.fetch_one(task_id=task_id,
            ebay_store_id=ebay_store_id,
            asin=asin)
        if not t:
            AmazonScrapeTaskModelManager.create(
                task_id=task_id,
                ebay_store_id=ebay_store_id,
                asin=asin,
                parent_asin=parent_asin)
        return True

    def process_item(self, item, spider):
        if isinstance(item, AmazonScrapyItem): # AmazonItem (scrapy item)
            _add_to_scrape_task = True
            if not hasattr(spider, 'task_id') or not spider.task_id:
                _add_to_scrape_task = False
            elif not hasattr(spider, 'ebay_store_id') or not spider.ebay_store_id:
                _add_to_scrape_task = False
            elif hasattr(spider, 'max_amazon_price') and spider.max_amazon_price and item.get('price', None) and amazonmws_utils.number_to_dcmlprice(item.get('price')) > spider.max_amazon_price:
                _add_to_scrape_task = False
            elif hasattr(spider, 'min_amazon_price') and spider.min_amazon_price and item.get('price', None) and amazonmws_utils.number_to_dcmlprice(item.get('price')) < spider.min_amazon_price:
                _add_to_scrape_task = False
            elif not AmazonItemModelManager.fetch_one(asin=item.get('asin', '')):
                _add_to_scrape_task = False

            if _add_to_scrape_task:
                self.__handle_redirected_asins(redirected_asins=item.get('_redirected_asins', {}),
                    task_id=spider.task_id,
                    ebay_store_id=spider.ebay_store_id)
                self.__store_amazon_scrape_tasks(task_id=spider.task_id,
                    ebay_store_id=spider.ebay_store_id,
                    asin=item.get('asin'),
                    parent_asin=item.get('parent_asin') if item.get('parent_asin') else item.get('asin'))
        return item


class DBPipeline(object):

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

    def __store_amazon_apparel_item(self, item):
        apparel = AmazonItemApparelModelManager.fetch_one(parent_asin=item.get('parent_asin'))
        if not apparel:
            AmazonItemApparelModelManager.create(parent_asin=item.get('parent_asin'),
                size_chart=item.get('size_chart', None))
        else:
            AmazonItemApparelModelManager.update(apparel,
                size_chart=item.get('size_chart', None))
        return True

    def process_item(self, item, spider):
        if isinstance(item, AmazonBestsellerScrapyItem): # AmazonBestsellerItem (scrapy item)
            self.__store_amazon_bestseller_item(item)
        elif isinstance(item, AmazonOfferScrapyItem): # AmazonOfferItem (scrapy item)
            self.__store_amazon_offer_item(item)
        elif isinstance(item, AmazonApparelScrapyItem): # AmazonApparelItem (scrapy item)
            self.__store_amazon_apparel_item(item)
        return item

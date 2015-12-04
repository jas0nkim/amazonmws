import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

import datetime

from storm.expr import Select, And, Desc, Not, SQLRaw
from storm.exceptions import StormError

from amazonmws import settings
from amazonmws.models import StormStore, EbayStore, EbayItem, Transaction, zzAmazonItem as AmazonItem, zzAmazonItemPicture as AmazonItemPicture, zzAtoECategoryMap as AtoECategoryMap, zzAmazonItemOffer as AmazonItemOffer, zzAmazonBestsellers as AmazonBestsellers,zzEbayStorePreferredCategory as EbayStorePreferredCategory, zzExclBrand as ExclBrand
from amazonmws.loggers import GrayLogger as logger


class AmazonItemModelManager(object):

    @staticmethod
    def create(**kw):
        try:
            item = AmazonItem()
            item.asin = kw['asin'] if 'asin' in kw else item.asin
            item.url = kw['url'] if 'url' in kw else item.url
            item.category = kw['category'] if 'category' in kw else item.category
            item.title = kw['title'] if 'title' in kw else item.title
            item.price = kw['price'] if 'price' in kw else item.price
            item.market_price = kw['market_price'] if 'market_price' in kw else item.market_price
            item.quantity = kw['quantity'] if 'quantity' in kw else item.quantity
            item.features = kw['features'] if 'features' in kw else item.features
            item.description = kw['description'] if 'description' in kw else item.description
            item.review_count = kw['review_count'] if 'review_count' in kw else item.review_count
            item.avg_rating = kw['avg_rating'] if 'avg_rating' in kw else item.avg_rating
            item.is_fba = kw['is_fba'] if 'is_fba' in kw else item.is_fba
            item.is_addon = kw['is_addon'] if 'is_addon' in kw else item.is_addon
            item.merchant_id = kw['merchant_id'] if 'merchant_id' in kw else item.merchant_id
            item.merchant_name = kw['merchant_name'] if 'merchant_name' in kw else item.merchant_name
            item.brand_name = kw['brand_name'] if 'brand_name' in kw else item.brand_name
            item.status = kw['status'] if 'status' in kw else item.status
            item.created_at = datetime.datetime.now()
            item.updated_at = datetime.datetime.now()
            
            StormStore.add(item)
            StormStore.commit()
            return True
        except StormError, e:
            StormStore.rollback()
            logger.exception(e)
            return False
        except Exception, e:
            StormStore.rollback()
            logger.exception(e)
            return False

    @staticmethod
    def update(item, **kw):
        try:
            item.url = kw['url'] if 'url' in kw else item.url
            item.category = kw['category'] if 'category' in kw else item.category
            item.title = kw['title'] if 'title' in kw else item.title
            item.price = kw['price'] if 'price' in kw else item.price
            item.market_price = kw['market_price'] if 'market_price' in kw else item.market_price
            item.quantity = kw['quantity'] if 'quantity' in kw else item.quantity
            item.features = kw['features'] if 'features' in kw else item.features
            item.description = kw['description'] if 'description' in kw else item.description
            item.review_count = kw['review_count'] if 'review_count' in kw else item.review_count
            item.avg_rating = kw['avg_rating'] if 'avg_rating' in kw else item.avg_rating
            item.is_fba = kw['is_fba'] if 'is_fba' in kw else item.is_fba
            item.is_addon = kw['is_addon'] if 'is_addon' in kw else item.is_addon
            item.merchant_id = kw['merchant_id'] if 'merchant_id' in kw else item.merchant_id
            item.merchant_name = kw['merchant_name'] if 'merchant_name' in kw else item.merchant_name
            item.brand_name = kw['brand_name'] if 'brand_name' in kw else item.brand_name
            item.status = kw['status'] if 'status' in kw else item.status
            item.updated_at = datetime.datetime.now()
            
            StormStore.add(item)
            StormStore.commit()
            return True
        except StormError, e:
            StormStore.rollback()
            logger.exception(e)
            return False
        except Exception, e:
            StormStore.rollback()
            logger.exception(e)
            return False

    @staticmethod
    def inactive(item):
        try:
            item.status = AmazonItem.STATUS_INACTIVE
            item.updated_at = datetime.datetime.now()            
            StormStore.add(item)
            StormStore.commit()
            return True
        except StormError, e:
            StormStore.rollback()
            logger.exception(e)
            return False
        except Exception, e:
            StormStore.rollback()
            logger.exception(e)
            return False

    @staticmethod
    def fetch(**kw):
        expressions = []
        if 'is_fba' in kw:
            expressions += [ AmazonItem.is_fba == kw['is_fba'] ]
        if 'is_addon' in kw:
            expressions += [ AmazonItem.is_addon == kw['is_addon'] ]
        if 'merchant_id' in kw:
            expressions += [ AmazonItem.merchant_id == kw['merchant_id'] ]
        if 'brand_name' in kw:
            expressions += [ AmazonItem.brand_name == kw['brand_name'] ]
        if len(expressions) > 0:
            return StormStore.find(AmazonItem, And(*expressions))
        else:
            return StormStore.find(AmazonItem)

    @staticmethod
    def fetch_one(asin):
        try:
            ret = StormStore.find(AmazonItem, AmazonItem.asin == asin).one()
        except StormError, e:
            ret = None
        return ret

    @staticmethod
    def fetch_sold_for_listing(ebay_store):
        """fetch amazon items which sold by sellers in system - order by num of sold
        """
        ret = []
        query = 'SELECT c.asin, COUNT(*) as count FROM %s a LEFT JOIN %s b ON a.item_id = b.ebid LEFT JOIN %s c ON b.asin = c.asin WHERE c.asin IS NOT NULL GROUP BY b.asin ORDER BY count DESC' % (Transaction.__storm_table__, EbayItem.__storm_table__, AmazonItem.__storm_table__)

        results = StormStore.execute(SQLRaw("(%s)" % query)).get_all()
        num_items = 0
        if len(results) > 0:
            for result in results:
                amazon_item = None
                ebay_item = None
                try:
                    amazon_item = StormStore.find(AmazonItem, 
                        AmazonItem.asin == result[0]).one()
                except StormError, e:
                    logger.exception(e)
                    continue
                try:
                    ebay_item = StormStore.find(EbayItem,
                        EbayItem.ebay_store_id == ebay_store.id,
                        EbayItem.asin == result[0]).one()
                except StormError, e:
                    logger.exception(e)
                ret.append((amazon_item, ebay_item))
                num_items += 1

        logger.info("[ebay store id:%s] Number of items to list on ebay: %d items" % (ebay_store.id, num_items))
        return ret

    @staticmethod
    def fetch_filtered_for_listing(preferred_category, min_review_count, **kw):
        """filter amazon item by given a preferred category of a ebay store:
            - amazon active items
            - FBA items
            - not add-on items
            - item which has not listed at ebay store
            return type: list
        """

        result = []
        filtered_items = []
        try:
            expressions = []
            if preferred_category.category_type == 'amazon':
                expressions += [ AmazonItem.category.startswith(preferred_category.category_name) ]
                expressions += [ AmazonItem.status == AmazonItem.STATUS_ACTIVE ]
                expressions += [ AmazonItem.is_fba == True ]
                expressions += [ AmazonItem.is_addon == False ]
                expressions += [ AmazonItem.quantity >= settings.AMAZON_MINIMUM_QUANTITY_FOR_LISTING ]
                expressions += [ AmazonItem.review_count >= min_review_count ]
                if 'asins_exclude' in kw:
                    expressions += [ Not(AmazonItem.asin.is_in(kw['asins_exclude'])) ]
                if 'listing_min_dollar' in kw and kw['listing_min_dollar'] != None:
                    expressions += [ AmazonItem.price >= kw['listing_min_dollar'] ]
                if 'listing_max_dollar' in kw and kw['listing_max_dollar'] != None:
                    expressions += [ AmazonItem.price <= kw['listing_max_dollar'] ]

                filtered_items = StormStore.find(AmazonItem, 
                    And(*expressions)
                ).order_by(Desc(AmazonItem.avg_rating), 
                    Desc(AmazonItem.review_count))
            else: # amazon_bestseller
                expressions += [ AmazonItem.asin == AmazonBestsellers.asin ]
                expressions += [ AmazonItem.status == AmazonItem.STATUS_ACTIVE ]
                expressions += [ AmazonItem.is_fba == True ]
                expressions += [ AmazonItem.is_addon == False ]
                expressions += [ AmazonItem.quantity >= settings.AMAZON_MINIMUM_QUANTITY_FOR_LISTING ]
                if 'asins_exclude' in kw:
                    expressions += [ Not(AmazonItem.asin.is_in(kw['asins_exclude'])) ]
                if 'listing_min_dollar' in kw and kw['listing_min_dollar'] != None:
                    expressions += [ AmazonItem.price >= kw['listing_min_dollar'] ]
                if 'listing_max_dollar' in kw and kw['listing_max_dollar'] != None:
                    expressions += [ AmazonItem.price <= kw['listing_max_dollar'] ]

                filtered_items = StormStore.find(AmazonItem, 
                    And(*expressions)
                ).order_by(AmazonBestsellers.rank)
        except StormError:
            logger.exception('Unable to filter amazon items')

        # workaround solution - stupid but storm doesn't support outer join...
        # what it supposes to do - i.e.
        #   SELECT * FROM pets AS p 
        #       LEFT OUTER JOIN lost-pets AS lp
        #       ON p.name = lp.name
        #       WHERE lp.id IS NULL
        #       
        # ref: http://stackoverflow.com/a/369861
        num_items = 0

        for amazon_item in filtered_items:
            # ebay_item
            ebay_item = None
            try:
                ebay_item = StormStore.find(EbayItem, 
                    EbayItem.ebay_store_id == preferred_category.ebay_store_id,
                    EbayItem.asin == amazon_item.asin).one()
            except StormError, e:
                logger.exception(e)

            if not ebay_item:
                num_items += 1
                item_set = (amazon_item, None)
                result.append(item_set)
            elif ebay_item.status == EbayItem.STATUS_OUT_OF_STOCK:
                """add OOS ebay item - need to restock to ebay because it's been restocked on amazon!
                """
                num_items += 1
                item_set = (amazon_item, ebay_item)
                result.append(item_set)

        logger.info("[ebay store id:%s] Number of items to list on ebay: %d items" % (preferred_category.ebay_store_id, num_items))
        return result

class AmazonItemPictureModelManager(object):

    @staticmethod
    def create(**kw):
        try:
            picture = AmazonItemPicture()
            picture.asin = kw['asin'] if 'asin' in kw else picture.asin
            picture.picture_url = kw['picture_url'] if 'picture_url' in kw else picture.picture_url
            picture.created_at = datetime.datetime.now()
            picture.updated_at = datetime.datetime.now()

            StormStore.add(picture)
            StormStore.commit()

            return True
        except StormError, e:
            StormStore.rollback()
            logger.exception(e)
            return False
        except Exception, e:
            StormStore.rollback()
            logger.exception(e)
            return False

    @staticmethod
    def fetch_one(asin, picture_url):
        try:
            return StormStore.find(AmazonItemPicture, 
                AmazonItemPicture.asin == asin,
                AmazonItemPicture.picture_url == picture_url).one()
        except StormError, e:
            return None
        except Exception, e:
            return None

class AmazonBestsellersModelManager(object):

    @staticmethod
    def create(**kw):
        try:
            bestseller = AmazonBestsellers()
            bestseller.asin = kw['asin'] if 'asin' in kw else bestseller.asin
            bestseller.bestseller_category = kw['bestseller_category'] if 'bestseller_category' in kw else bestseller.bestseller_category
            bestseller.bestseller_category_url = kw['bestseller_category_url'] if 'bestseller_category_url' in kw else bestseller.bestseller_category_url
            bestseller.rank = kw['rank'] if 'rank' in kw else bestseller.rank
            bestseller.created_at = datetime.datetime.now()
            bestseller.updated_at = datetime.datetime.now()

            StormStore.add(bestseller)
            StormStore.commit()
            return True
        except StormError, e:
            StormStore.rollback()
            logger.exception(e)
            return False
        except Exception, e:
            StormStore.rollback()
            logger.exception(e)
            return False

    @staticmethod
    def update(bestseller, **kw):
        try:
            bestseller.asin = kw['asin'] if 'asin' in kw else bestseller.asin
            bestseller.bestseller_category = kw['bestseller_category'] if 'bestseller_category' in kw else bestseller.bestseller_category
            bestseller.updated_at = datetime.datetime.now()

            StormStore.add(bestseller)
            StormStore.commit()
            return True
        except StormError, e:
            StormStore.rollback()
            logger.exception(e)
            return False
        except Exception, e:
            StormStore.rollback()
            logger.exception(e)
            return False

    @staticmethod
    def fetch_one(bestseller_category_url, rank):
        try:
            return StormStore.find(AmazonBestsellers, 
                AmazonBestsellers.bestseller_category_url == bestseller_category_url,
                AmazonBestsellers.rank == rank).one()
        except StormError, e:
            return None
        except Exception, e:
            return None

    @staticmethod
    def fetch(**kw):
        expressions = []
        if 'category' in kw:
            expressions += [ AmazonBestsellers.bestseller_category == kw['category'] ]
        if len(expressions) > 0:
            return StormStore.find(AmazonBestsellers, And(*expressions))
        else:
            return StormStore.find(AmazonBestsellers)

class AmazonItemOfferModelManager(object):

    @staticmethod
    def create(**kw):
        try:
            offer = AmazonItemOffer()
            offer.asin = kw['asin'] if 'asin' in kw else offer.asin
            offer.price = kw['price'] if 'price' in kw else offer.price
            offer.quantity = kw['quantity'] if 'quantity' in kw else offer.quantity
            offer.is_fba = kw['is_fba'] if 'is_fba' in kw else offer.is_fba
            offer.merchant_id = kw['merchant_id'] if 'merchant_id' in kw else offer.merchant_id
            offer.merchant_name = kw['merchant_name'] if 'merchant_name' in kw else offer.merchant_name
            offer.revision = kw['revision'] if 'revision' in kw else offer.revision
            offer.created_at = datetime.datetime.now()
            offer.updated_at = datetime.datetime.now()

            StormStore.add(offer)
            StormStore.commit()
            return True
        except StormError, e:
            StormStore.rollback()
            logger.exception(e)
            return False
        except Exception, e:
            StormStore.rollback()
            logger.exception(e)
            return False

    @staticmethod
    def update(offer, **kw):
        try:
            offer.price = kw['price'] if 'price' in kw else offer.price
            offer.quantity = kw['quantity'] if 'quantity' in kw else offer.quantity
            offer.revision = kw['revision'] if 'revision' in kw else offer.revision
            offer.created_at = datetime.datetime.now()
            offer.updated_at = datetime.datetime.now()

            StormStore.add(offer)
            StormStore.commit()
            return True
        except StormError, e:
            StormStore.rollback()
            logger.exception(e)
            return False
        except Exception, e:
            StormStore.rollback()
            logger.exception(e)
            return False

    @staticmethod
    def fetch_one(asin, is_fba, merchant_id, merchant_name):
        try:
            return StormStore.find(AmazonItemOffer,
                AmazonItemOffer.asin == asin,
                AmazonItemOffer.is_fba == is_fba,
                AmazonItemOffer.merchant_id == merchant_id,
                AmazonItemOffer.merchant_name == merchant_name).one()
        except StormError, e:
            return None
        except Exception, e:
            return None


class AtoECategoryMapModelManager(object):

    @staticmethod
    def fetch():
        return StormStore.find(AtoECategoryMap)

    @staticmethod
    def fetch_one(amazon_category):
        try:
            ret = StormStore.find(AtoECategoryMap, 
                AtoECategoryMap.amazon_category == amazon_category).one()
        except StormError, e:
            logger.exception(e)
            ret = None
        return ret

    @staticmethod
    def create(amazon_category, **kw):
        try:
            cmap = AtoECategoryMap()
            cmap.amazon_category = amazon_category
            if 'ebay_category_id' in kw and kw['ebay_category_id'] != None:
                cmap.ebay_category_id = unicode(kw['ebay_category_id'])
            if 'ebay_category_name' in kw and kw['ebay_category_name'] != None:
                cmap.ebay_category_name = unicode(kw['ebay_category_name'])
            cmap.created_at = datetime.datetime.now()
            cmap.updated_at = datetime.datetime.now()
            StormStore.add(cmap)
            StormStore.commit()
            return True
        except StormError, e:
            StormStore.rollback()
            logger.exception("[AtoECategoryMapModelManager] Failed to store information on create new amazon to ebay category map - amazon category - %s" % amazon_category)
            return False

    @staticmethod
    def update(cmap, **kw):
        try:
            if 'ebay_category_id' in kw and kw['ebay_category_id'] != None:
                cmap.ebay_category_id = unicode(kw['ebay_category_id'])
            if 'ebay_category_name' in kw and kw['ebay_category_name'] != None:
                cmap.ebay_category_name = unicode(kw['ebay_category_name'])
            cmap.updated_at = datetime.datetime.now()
            StormStore.add(cmap)
            StormStore.commit()
            return True
        except StormError, e:
            StormStore.rollback()
            logger.exception("[AtoECategoryMapModelManager] Failed to store information on update amazon to ebay category map")
            return False


class ExclBrandModelManager(object):

    @staticmethod
    def fetch():
        return StormStore.find(ExclBrand)

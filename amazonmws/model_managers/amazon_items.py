import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'rfi'))

import datetime

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from amazonmws import settings
from amazonmws.loggers import GrayLogger as logger

from rfi_sources.models import AmazonItem, AmazonItemPicture, AmazonItemOffer, AToECategoryMap, AmazonBestseller
from rfi_orders.models import Transaction

class AmazonItemModelManager(object):

    @staticmethod
    def create(**kw):
        obj, created = AmazonItem.objects.update_or_create(**kw)
        return created

    @staticmethod
    def update(item, **kw):
        if isinstance(item, AmazonItem):
            item.update(**kw)
            return True
        return False

    @staticmethod
    def inactive(item):
        return AmazonItemModelManager.update(item, status=AmazonItem.STATUS_INACTIVE)        

    @staticmethod
    def fetch(**kw):
        # make compatible with django query
        if 'category_startswith' in kw:
            kw['category__startswith'] = kw['category_startswith']
            del kw['category_startswith']
        
        return AmazonItem.objects.filter(**kw)

    @staticmethod
    def fetch_one(asin):
        try:
            return AmazonItem.objects.get(asin=asin)
        except MultipleObjectsReturned as e:
            logger.error("[ASIN:%s] Multiple amazon item exists in the system" % asin)
            return None
        except ObjectDoesNotExist as e:
            logger.error("[ASIN:%s] Amazon item does not exist in the system" % asin)
            return None

    @staticmethod
    def _fetch_for_listing(results, ebay_store):
        ret = []
        num_items = 0
        if len(results) > 0:
            for result in results:

                print result

                amazon_item = None
                ebay_item = None
                
                try:
                    amazon_item = AmazonItem.objects.get(asin=result.asin)
                except StormError as e:
                    logger.exception(e)
                    continue
                
                if not amazon_item:
                    continue
                
                try:
                    ebay_item = StormStore.find(EbayItem,
                        EbayItem.ebay_store_id == ebay_store.id,
                        EbayItem.asin == result[0]).one()
                except StormError as e:
                    logger.exception(e)
                
                if not ebay_item:
                    num_items += 1
                    ret.append((amazon_item, None))
                elif ebay_item.status == EbayItem.STATUS_OUT_OF_STOCK:
                    """add OOS ebay item - need to restock to ebay because it's been restocked on amazon!
                    """
                    num_items += 1
                    ret.append((amazon_item, ebay_item))

        logger.info("[ebay store id:%s] Number of items to list on ebay: %d items" % (ebay_store.id, num_items))
        return ret

    @staticmethod
    def fetch_sold_for_listing(ebay_store, order='most'):
        """fetch amazon items which sold by sellers in our system
            order: most | recent
                - most: most sold item first
                - recent: recent sold item first
        """
        if order == 'recent':
            query = 'SELECT c.asin, a.created_at AS tran_created_at  FROM {table_transactions} a LEFT JOIN {table_ebay_items} b ON a.item_id = b.ebid LEFT JOIN {table_amazon_items} c ON b.asin = c.asin WHERE c.asin IS NOT NULL AND c.status = {status} AND c.is_fba = {is_fba} AND c.is_addon = {is_addon} AND c.is_pantry = {is_pantry} AND c.quantity >= {quantity} AND c.price >= {listing_min_dollar} AND c.price <= {listing_max_dollar} ORDER BY tran_created_at DESC'.format(
                    table_transactions=Transaction.Meta.db_table,
                    table_ebay_items=EbayItem.Meta.db_table, 
                    table_amazon_items=AmazonItem.Meta.db_table, 
                    status=AmazonItem.STATUS_ACTIVE, 
                    is_fba=1, 
                    is_addon=0, 
                    is_pantry=0,
                    quantity=settings.AMAZON_MINIMUM_QUANTITY_FOR_LISTING,
                    listing_min_dollar=float(ebay_store.listing_min_dollar) if ebay_store.listing_min_dollar else 0.00, 
                    listing_max_dollar=float(ebay_store.listing_max_dollar) if ebay_store.listing_max_dollar else 999999999.99)
        else: # most
            """ differ from previous query: has GROUP BY asin, and ORDER BY count... that's it
            """
            query = 'SELECT c.asin, COUNT(*) AS count FROM {table_transactions} a LEFT JOIN {table_ebay_items} b ON a.item_id = b.ebid LEFT JOIN {table_amazon_items} c ON b.asin = c.asin WHERE c.asin IS NOT NULL AND c.status = {status} AND c.is_fba = {is_fba} AND c.is_addon = {is_addon} AND c.is_pantry = {is_pantry} AND c.quantity >= {quantity} AND c.price >= {listing_min_dollar} AND c.price <= {listing_max_dollar} GROUP BY b.asin ORDER BY count DESC'.format(
                    table_transactions=Transaction.Meta.db_table,
                    table_ebay_items=EbayItem.Meta.db_table, 
                    table_amazon_items=AmazonItem.Meta.db_table, 
                    status=AmazonItem.STATUS_ACTIVE, 
                    is_fba=1, 
                    is_addon=0, 
                    is_pantry=0, 
                    quantity=settings.AMAZON_MINIMUM_QUANTITY_FOR_LISTING,
                    listing_min_dollar=float(ebay_store.listing_min_dollar) if ebay_store.listing_min_dollar else 0.00, 
                    listing_max_dollar=float(ebay_store.listing_max_dollar) if ebay_store.listing_max_dollar else 999999999.99)

        results = Transaction.objects.raw(query)
        return AmazonItemModelManager._fetch_for_listing(results, ebay_store)

    @staticmethod
    def fetch_discount_for_listing(ebay_store):
        """fetch amazon items have most discount
        """
        query = 'SELECT asin, ((market_price - price) / market_price * 100) AS discount FROM {table_amazon_items} WHERE status = {status} AND is_fba = {is_fba} AND is_addon = {is_addon} AND is_pantry = {is_pantry} AND quantity >= {quantity} AND price >= {listing_min_dollar} AND price <= {listing_max_dollar} ORDER BY discount DESC'.format(
                table_amazon_items=AmazonItem.Meta.db_table, 
                status=AmazonItem.STATUS_ACTIVE, 
                is_fba=1, 
                is_addon=0, 
                is_pantry=0, 
                quantity=settings.AMAZON_MINIMUM_QUANTITY_FOR_LISTING,
                listing_min_dollar=float(ebay_store.listing_min_dollar) if ebay_store.listing_min_dollar else 0.00, 
                listing_max_dollar=float(ebay_store.listing_max_dollar) if ebay_store.listing_max_dollar else 999999999.99)

        results = Transaction.objects.raw(query)
        return AmazonItemModelManager._fetch_for_listing(results, ebay_store)

    @staticmethod
    def fetch_filtered_for_listing(preferred_category, min_review_count, **kw):
        pass


class AmazonItemPictureModelManager(object):

    @staticmethod
    def create(**kw):
        pass

    @staticmethod
    def fetch_one(asin, picture_url):
        pass


class AmazonBestsellersModelManager(object):

    @staticmethod
    def create(**kw):
        pass

    @staticmethod
    def update(bestseller, **kw):
        pass
    
    @staticmethod
    def fetch_one(bestseller_category_url, rank):
        pass

    @staticmethod
    def fetch(**kw):
        pass


class AmazonItemOfferModelManager(object):

    @staticmethod
    def create(**kw):
        pass

    @staticmethod
    def update(offer, **kw):
        pass

    @staticmethod
    def fetch_one(asin, is_fba, merchant_id, merchant_name):
        pass


class AtoECategoryMapModelManager(object):

    @staticmethod
    def fetch(**kw):
        pass

    @staticmethod
    def fetch_one(amazon_category):
        pass

    @staticmethod
    def create(amazon_category, **kw):
        pass

    @staticmethod
    def update(cmap, **kw):
        pass


class ExclBrandModelManager(object):

    @staticmethod
    def fetch():
        pass        

import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'rfi'))

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from amazonmws import settings
from amazonmws.loggers import GrayLogger as logger

from rfi_sources.models import AmazonItem, AmazonItemPicture, AmazonItemOffer, AToECategoryMap, AmazonBestseller
from rfi_listings.models import EbayItem, ExclBrand
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
                except MultipleObjectsReturned as e:
                    logger.exception(e)
                    continue
                except DoesNotExist as e:
                    logger.exception(e)
                    continue
                
                if not amazon_item:
                    continue
                
                try:
                    ebay_item = EbayItem.objects.get(
                        ebay_store_id=ebay_store.id,
                        asin=result.asin
                    )
                except MultipleObjectsReturned as e:
                    logger.exception(e)
                    continue
                except DoesNotExist as e:
                    logger.exception(e)
                    continue
                
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
        """filter amazon item by given a preferred category of a ebay store:
            - amazon active items
            - FBA items
            - not add-on items
            - item which has not listed at ebay store
            return type: list
        """
        result = []
        filtered_amazon_items = AmazonItem.objects.filter(
            status=AmazonItem.STATUS_ACTIVE,
            is_fba=True,
            is_addon=False,
            is_pantry=False,
            quantity__gte=settings.AMAZON_MINIMUM_QUANTITY_FOR_LISTING
        )
        if min_review_count:
            filtered_amazon_items = filtered_amazon_items.filter(review_count__gte=min_review_count)
        if 'asins_exclude' in kw:
            filtered_amazon_items = filtered_amazon_items.exclude(asin__in=kw['asins_exclude'])
        if 'listing_min_dollar' in kw and kw['listing_min_dollar'] != None:
            filtered_amazon_items = filtered_amazon_items.exclude(price__gte=kw['listing_min_dollar'])
        if 'listing_max_dollar' in kw and kw['listing_max_dollar'] != None:
            filtered_amazon_items = filtered_amazon_items.exclude(price__lte=kw['listing_max_dollar'])

        if preferred_category.category_type == 'amazon':
            filtered_amazon_items = filtered_amazon_items.filter(category__startswith=preferred_category.category_name)
            filtered_amazon_items = filtered_amazon_items.order_by('-avg_rating', '-review_count')
        else: # amazon_bestseller
            filtered_amazon_items = filtered_amazon_items.filter(amazon_bestsellers__bestseller_category=preferred_category.category_name)
            filtered_amazon_items = filtered_amazon_items.order_by('amazon_bestsellers__rank')


        # workaround solution - outer join...
        # what it supposes to do - i.e.
        #   SELECT * FROM pets AS p 
        #       LEFT OUTER JOIN lost-pets AS lp
        #       ON p.name = lp.name
        #       WHERE lp.id IS NULL
        #       
        # ref: http://stackoverflow.com/a/369861
        num_items = 0

        for amazon_item in filtered_amazon_items:
            # ebay_item
            ebay_item = None
            try:
                ebay_item = EbayItem.objects.get(
                    ebay_store_id=preferred_category.ebay_store_id,
                    asin=amazon_item.asin
                )
            except MultipleObjectsReturned as e:
                logger.exception(e)
            except DoesNotExist as e:
                logger.exception(e)

            if not ebay_item:
                num_items += 1
                result.append((amazon_item, None))
            elif ebay_item.status == EbayItem.STATUS_OUT_OF_STOCK:
                """add OOS ebay item - need to restock to ebay because it's been restocked on amazon!
                """
                num_items += 1
                result.append((amazon_item, ebay_item))

        logger.info("[ebay store id:%s] Number of items to list on ebay: %d items" % (preferred_category.ebay_store_id, num_items))
        return result


class AmazonItemPictureModelManager(object):

    @staticmethod
    def create(**kw):
        obj, created = AmazonItemPicture.objects.update_or_create(**kw)
        return created

    @staticmethod
    def fetch_one(asin, picture_url):
        try:
            return AmazonItemPicture.objects.get(
                asin=asin,
                picture_url=picture_url
            )
        except MultipleObjectsReturned as e:
            logger.exception(e)
            return None
        except DoesNotExist as e:
            logger.exception(e)
            return None


class AmazonBestsellersModelManager(object):

    @staticmethod
    def create(**kw):
        obj, created = AmazonBestseller.objects.update_or_create(**kw)
        return created

    @staticmethod
    def update(bestseller, **kw):
        if isinstance(bestseller, AmazonBestseller):
            bestseller.update(**kw)
            return True
        return False
    
    @staticmethod
    def fetch_one(bestseller_category_url, rank):
        try:
            return AmazonBestseller.objects.get(
                bestseller_category_url=bestseller_category_url,
                rank=rank
            )
        except MultipleObjectsReturned as e:
            logger.exception(e)
            return None
        except DoesNotExist as e:
            logger.exception(e)
            return None

    @staticmethod
    def fetch(**kw):
        # make compatible with django query
        if 'category' in kw:
            kw['bestseller_category'] = kw['category']
            del kw['category']

        return AmazonBestseller.objects.filter(**kw)


class AmazonItemOfferModelManager(object):

    @staticmethod
    def create(**kw):
        obj, created = AmazonItemOffer.objects.update_or_create(**kw)
        return created

    @staticmethod
    def update(offer, **kw):
        if isinstance(offer, AmazonItemOffer):
            offer.update(**kw)
            return True
        return False

    @staticmethod
    def fetch_one(asin, is_fba, merchant_id, merchant_name):
        try:
            return AmazonItemOffer.objects.get(
                asin=asin,
                is_fba=is_fba,
                merchant_id=merchant_id,
                merchant_name=merchant_name
            )
        except MultipleObjectsReturned as e:
            logger.exception(e)
            return None
        except DoesNotExist as e:
            logger.exception(e)
            return None


class AtoECategoryMapModelManager(object):

    @staticmethod
    def fetch(**kw):
        # make compatible with django query
        return AToECategoryMap.objects.filter(**kw)

    @staticmethod
    def fetch_one(amazon_category):
        try:
            return AToECategoryMap.objects.get(amazon_category=amazon_category)
        except MultipleObjectsReturned as e:
            logger.exception(e)
            return None
        except DoesNotExist as e:
            logger.exception(e)
            return None

    @staticmethod
    def create(**kw):
        obj, created = AToECategoryMap.objects.update_or_create(**kw)
        return created

    @staticmethod
    def update(cmap, **kw):
        if isinstance(cmap, AToECategoryMap):
            cmap.update(**kw)
            return True
        return False


class ExclBrandModelManager(object):

    @staticmethod
    def fetch():
        return ExclBrand.objects.all()

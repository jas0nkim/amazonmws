import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'rfi'))

from django.core.exceptions import MultipleObjectsReturned

from amazonmws import settings
from amazonmws.loggers import GrayLogger as logger

from rfi_sources.models import *
from rfi_listings.models import EbayItem, ExclBrand
from rfi_orders.models import Transaction


class AmazonItemModelManager(object):

    @staticmethod
    def create(**kw):
        obj, created = AmazonItem.objects.update_or_create(**kw)
        if obj:
            """
                create entry for each of following:
                    AmazonItemPrice
                    AmazonItemMarketPrice
                    AmazonItemQuantity
                    AmazonItemTitle
                    AmazonItemDescription
                    AmazonItemFeature
            """
            AmazonItemPriceModelManager.create(asin=obj.asin,
                parent_asin=obj.parent_asin,
                price=obj.price)
            AmazonItemMarketPriceModelManager.create(asin=obj.asin,
                parent_asin=obj.parent_asin,
                market_price=obj.market_price)
            AmazonItemQuantityModelManager.create(asin=obj.asin,
                parent_asin=obj.parent_asin,
                quantity=obj.quantity)
            AmazonItemTitleModelManager.create(asin=obj.asin,
                parent_asin=obj.parent_asin,
                title=obj.title)
            AmazonItemDescriptionModelManager.create(asin=obj.asin,
                parent_asin=obj.parent_asin,
                description=obj.description)
            AmazonItemFeatureModelManager.create(asin=obj.asin,
                parent_asin=obj.parent_asin,
                features=obj.features)
        return created

    @staticmethod
    def update(item, **kw):
        if isinstance(item, AmazonItem):
            try:
                _is_price_updated = False
                _is_market_price_updated = False
                _is_quantity_updated = False
                _is_title_updated = False
                _is_description_updated = False
                _is_features_updated = False
                if 'price' in kw and item.price != kw['price']:
                    _is_price_updated = True
                if 'market_price' in kw and item.market_price != kw['market_price']:
                    _is_market_price_updated = True
                if 'quantity' in kw and item.quantity != kw['quantity']:
                    _is_quantity_updated = True
                if 'title' in kw and item.title != kw['title']:
                    _is_title_updated = True
                if 'description' in kw and item.description != kw['description']:
                    _is_description_updated = True
                if 'features' in kw and item.features != kw['features']:
                    _is_features_updated = True
                
                for key, value in kw.iteritems():
                    setattr(item, key, value)
                item.save()

                if _is_price_updated:
                    AmazonItemPriceModelManager.create(asin=item.asin,
                        parent_asin=item.parent_asin,
                        price=item.price)
                if _is_market_price_updated:
                    AmazonItemMarketPriceModelManager.create(asin=item.asin,
                        parent_asin=item.parent_asin,
                        market_price=item.market_price)
                if _is_quantity_updated:
                    AmazonItemQuantityModelManager.create(asin=item.asin,
                        parent_asin=item.parent_asin,
                        quantity=item.quantity)
                if _is_title_updated:
                    AmazonItemTitleModelManager.create(asin=item.asin,
                        parent_asin=item.parent_asin,
                        title=item.title)
                if _is_description_updated:
                    AmazonItemDescriptionModelManager.create(asin=item.asin,
                        parent_asin=item.parent_asin,
                        description=item.description)
                if _is_features_updated:
                    AmazonItemFeatureModelManager.create(asin=item.asin,
                        parent_asin=item.parent_asin,
                        features=item.features)

            except Exception as e:
                logger.error("[Database Error] {e}".format(e=str(e)))
                return False
            return True
        return False

    @staticmethod
    def inactive(item):
        return AmazonItemModelManager.update(item, status=AmazonItem.STATUS_INACTIVE)        

    @staticmethod
    def oos(item):
        return AmazonItemModelManager.update(item, quantity=0)

    @staticmethod
    def fetch(**kw):
        # make compatible with django query
        if 'category_startswith' in kw:
            kw['category__startswith'] = kw['category_startswith']
            kw.pop('category_startswith', None)
        
        return AmazonItem.objects.filter(**kw)

    @staticmethod
    def fetch_one(asin, **kw):
        try:
            return AmazonItem.objects.get(asin=asin, **kw)
        except MultipleObjectsReturned as e:
            logger.error("[ASIN:%s] Multiple amazon item exists in the system" % asin)
            return None
        except AmazonItem.DoesNotExist as e:
            logger.warning("[ASIN:%s] Amazon item does not exist in the system. Create one!" % asin)
            return None

    @staticmethod
    def _fetch_for_listing(results, ebay_store):
        ret = []
        num_items = 0
        for result in results:
            amazon_item = None
            ebay_item = None
            
            try:
                amazon_item = AmazonItem.objects.get(asin=result.asin)
            except MultipleObjectsReturned as e:
                logger.exception(e)
                continue
            except AmazonItem.DoesNotExist as e:
                logger.exception(e)
                continue
            
            if not amazon_item:
                continue
            
            try:
                ebay_item = EbayItem.objects.get(
                    ebay_store=ebay_store,
                    amazon_item=amazon_item
                )
            except MultipleObjectsReturned as e:
                logger.exception(e)
                ebay_item = None
            except EbayItem.DoesNotExist as e:
                logger.exception(e)
                ebay_item = None
            
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
            query = 'SELECT c.id, c.asin, a.created_at AS tran_created_at  FROM {table_transactions} a LEFT JOIN {table_ebay_items} b ON a.item_id = b.ebid LEFT JOIN {table_amazon_items} c ON b.asin = c.asin WHERE c.asin IS NOT NULL AND c.status = {status} AND c.is_fba = {is_fba} AND c.is_addon = {is_addon} AND c.is_pantry = {is_pantry} AND c.quantity >= {quantity} AND c.price >= {listing_min_dollar} AND c.price <= {listing_max_dollar} ORDER BY tran_created_at DESC'.format(
                    table_transactions=Transaction._meta.db_table,
                    table_ebay_items=EbayItem._meta.db_table, 
                    table_amazon_items=AmazonItem._meta.db_table, 
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
            query = 'SELECT c.id, c.asin, COUNT(*) AS count FROM {table_transactions} a LEFT JOIN {table_ebay_items} b ON a.item_id = b.ebid LEFT JOIN {table_amazon_items} c ON b.asin = c.asin WHERE c.asin IS NOT NULL AND c.status = {status} AND c.is_fba = {is_fba} AND c.is_addon = {is_addon} AND c.is_pantry = {is_pantry} AND c.quantity >= {quantity} AND c.price >= {listing_min_dollar} AND c.price <= {listing_max_dollar} GROUP BY b.asin ORDER BY count DESC'.format(
                    table_transactions=Transaction._meta.db_table,
                    table_ebay_items=EbayItem._meta.db_table, 
                    table_amazon_items=AmazonItem._meta.db_table, 
                    status=AmazonItem.STATUS_ACTIVE, 
                    is_fba=1, 
                    is_addon=0, 
                    is_pantry=0, 
                    quantity=settings.AMAZON_MINIMUM_QUANTITY_FOR_LISTING,
                    listing_min_dollar=float(ebay_store.listing_min_dollar) if ebay_store.listing_min_dollar else 0.00, 
                    listing_max_dollar=float(ebay_store.listing_max_dollar) if ebay_store.listing_max_dollar else 999999999.99)

        results = AmazonItem.objects.raw(query)
        return AmazonItemModelManager._fetch_for_listing(results, ebay_store)

    @staticmethod
    def fetch_discount_for_listing(ebay_store):
        """fetch amazon items have most discount
        """
        query = 'SELECT id, asin, ((market_price - price) / market_price * 100) AS discount FROM {table_amazon_items} WHERE status = {status} AND is_fba = {is_fba} AND is_addon = {is_addon} AND is_pantry = {is_pantry} AND quantity >= {quantity} AND price >= {listing_min_dollar} AND price <= {listing_max_dollar} ORDER BY discount DESC'.format(
                table_amazon_items=AmazonItem._meta.db_table, 
                status=AmazonItem.STATUS_ACTIVE, 
                is_fba=1, 
                is_addon=0, 
                is_pantry=0, 
                quantity=settings.AMAZON_MINIMUM_QUANTITY_FOR_LISTING,
                listing_min_dollar=float(ebay_store.listing_min_dollar) if ebay_store.listing_min_dollar else 0.00, 
                listing_max_dollar=float(ebay_store.listing_max_dollar) if ebay_store.listing_max_dollar else 999999999.99)

        results = AmazonItem.objects.raw(query)
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
            is_fba=1,
            is_addon=0,
            is_pantry=0,
            quantity__gte=settings.AMAZON_MINIMUM_QUANTITY_FOR_LISTING
        )
        if min_review_count:
            filtered_amazon_items = filtered_amazon_items.filter(review_count__gte=min_review_count)
        if 'asins_exclude' in kw:
            filtered_amazon_items = filtered_amazon_items.exclude(asin__in=kw['asins_exclude'])
        if 'listing_min_dollar' in kw and kw['listing_min_dollar'] != None:
            filtered_amazon_items = filtered_amazon_items.filter(price__gte=kw['listing_min_dollar'])
        if 'listing_max_dollar' in kw and kw['listing_max_dollar'] != None:
            filtered_amazon_items = filtered_amazon_items.filter(price__lte=kw['listing_max_dollar'])

        if preferred_category.category_type == 'amazon':
            filtered_amazon_items = filtered_amazon_items.filter(category__startswith=preferred_category.category_name)
            filtered_amazon_items = filtered_amazon_items.order_by('-avg_rating', '-review_count')
        else: # amazon_bestseller
            filtered_amazon_items = filtered_amazon_items.filter(
                asin__in=AmazonBestsellerModelManager.fetch(bestseller_category=preferred_category.category_name).order_by('rank').values_list('asin', flat=True).distinct()
            )

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
                    amazon_item=amazon_item
                )
            except MultipleObjectsReturned as e:
                logger.exception(e)
            except EbayItem.DoesNotExist as e:
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

    @staticmethod
    def find_parent_asin(asin):
        item = AmazonItemModelManager.fetch_one(asin=asin)
        if item:
            return item.parent_asin
        return None

    """ DEPRECATED
    """
    @staticmethod
    def fetch_distinct_parent_asins_apparel_only(**kw):
        return AmazonItemModelManager.fetch_apparel_only(**kw).values_list('parent_asin', flat=True).distinct()

    """ DEPRECATED
    """
    @staticmethod
    def fetch_apparel_only(**kw):
        return AmazonItem.objects.filter(category__icontains='clothing', **kw)

    @staticmethod
    def fetch_distinct_parent_asins_has_sizechart_only(**kw):
        return AmazonItem.objects.filter(has_sizechart=True, **kw).values_list('parent_asin', flat=True)

    @staticmethod
    def fetch_its_variations(parent_asin, **kw):
        kw['status'] = AmazonItem.STATUS_ACTIVE
        return AmazonItemModelManager.fetch(parent_asin=parent_asin, **kw)

    @staticmethod
    def fetch_its_variation_asins(parent_asin, **kw):
        return AmazonItemModelManager.fetch_its_variations(parent_asin=parent_asin, **kw).values_list('asin', flat=True).distinct()


class AmazonItemPictureModelManager(object):

    @staticmethod
    def create(**kw):
        obj, created = AmazonItemPicture.objects.update_or_create(**kw)
        return created

    @staticmethod
    def save_item_pictures(asin, picture_urls=[]):
        if len(picture_urls) < 1:
            return False
        # 1. delete all picture urls from db
        AmazonItemPicture.objects.filter(asin=asin).delete()
        # 2. update or create (update_or_create) given urls
        for pic_url in picture_urls:
            AmazonItemPictureModelManager.create(asin=asin, picture_url=pic_url)
        return True

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
        except AmazonItemPicture.DoesNotExist as e:
            logger.warning("[ASIN:%s|url:%s] - DoesNotExist: Amazon item picture does not exist. Create one!" % (asin, picture_url))
            return None

    @staticmethod
    def fetch(**kw):
        return AmazonItemPicture.objects.filter(**kw).order_by('id')


class AmazonItemPriceModelManager(object):

    @staticmethod
    def create(**kw):
        try:
            obj = AmazonItemPrice(**kw)
            obj.save()
        except Exception as e:
            logger.error("[Database Error] {e}".format(e=str(e)))
            return False
        return True


class AmazonItemMarketPriceModelManager(object):

    @staticmethod
    def create(**kw):
        try:
            obj = AmazonItemMarketPrice(**kw)
            obj.save()
        except Exception as e:
            logger.error("[Database Error] {e}".format(e=str(e)))
            return False
        return True


class AmazonItemQuantityModelManager(object):

    @staticmethod
    def create(**kw):
        try:
            obj = AmazonItemQuantity(**kw)
            obj.save()
        except Exception as e:
            logger.error("[Database Error] {e}".format(e=str(e)))
            return False
        return True


class AmazonItemTitleModelManager(object):

    @staticmethod
    def create(**kw):
        try:
            obj = AmazonItemTitle(**kw)
            obj.save()
        except Exception as e:
            logger.error("[Database Error] {e}".format(e=str(e)))
            return False
        return True


class AmazonItemDescriptionModelManager(object):

    @staticmethod
    def create(**kw):
        try:
            obj = AmazonItemDescription(**kw)
            obj.save()
        except Exception as e:
            logger.error("[Database Error] {e}".format(e=str(e)))
            return False
        return True


class AmazonItemFeatureModelManager(object):

    @staticmethod
    def create(**kw):
        try:
            obj = AmazonItemFeature(**kw)
            obj.save()
        except Exception as e:
            logger.error("[Database Error] {e}".format(e=str(e)))
            return False
        return True


class AmazonItemApparelModelManager(object):

    @staticmethod
    def create(**kw):
        obj, created = AmazonItemApparel.objects.update_or_create(**kw)
        return created

    @staticmethod
    def update(apparel, **kw):
        if isinstance(apparel, AmazonItemApparel):
            for key, value in kw.iteritems():
                setattr(apparel, key, value)
            apparel.save()
            return True
        return False

    @staticmethod
    def fetch_one(**kw):
        if 'parent_asin' in kw:
            try:
                return AmazonItemApparel.objects.get(parent_asin=kw['parent_asin'])
            except MultipleObjectsReturned as e:
                logger.error("[ASIN:%s] Multile asin exist" % kw['parent_asin'])
                return None
            except AmazonItemApparel.DoesNotExist as e:
                logger.warning("[ASIN:%s] - DoesNotExist: AmazonItemApparel matching query does not exist. Create one!" % kw['parent_asin'])
                return None
        else:
            return None

    @staticmethod
    def fetch(**kw):
        return AmazonItemApparel.objects.filter(**kw).order_by('id')

    @staticmethod
    def get_size_chart(parent_asin):
        a = AmazonItemApparelModelManager.fetch_one(parent_asin=parent_asin)
        if not a:
            return None
        if a.size_chart is None or a.size_chart == "":
            return None
        return a.size_chart


class AmazonBestsellerModelManager(object):

    @staticmethod
    def create(**kw):
        obj, created = AmazonBestseller.objects.update_or_create(**kw)
        return created

    @staticmethod
    def update(bestseller, **kw):
        if isinstance(bestseller, AmazonBestseller):
            for key, value in kw.iteritems():
                setattr(bestseller, key, value)
            bestseller.save()
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
        except AmazonBestseller.DoesNotExist as e:
            logger.warning('[{}|rank:{}] no bestseller record yet. create new now!'.format(bestseller_category_url, rank))
            return None

    @staticmethod
    def fetch(**kw):
        # make compatible with django query
        if 'category' in kw:
            kw['bestseller_category'] = kw['category']
            kw.pop('category', None)

        return AmazonBestseller.objects.filter(**kw)


class AmazonItemOfferModelManager(object):

    @staticmethod
    def create(**kw):
        obj, created = AmazonItemOffer.objects.update_or_create(**kw)
        return created

    @staticmethod
    def update(offer, **kw):
        if isinstance(offer, AmazonItemOffer):
            for key, value in kw.iteritems():
                setattr(offer, key, value)
            offer.save()
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
        except AmazonItemOffer.DoesNotExist as e:
            logger.exception(e)
            return None

    @staticmethod
    def fetch(**kw):
        return AmazonItem.objects.filter(**kw)


class AtoECategoryMapModelManager(object):

    @staticmethod
    def fetch(**kw):
        # make compatible with django query
        return AToECategoryMap.objects.filter(**kw)

    @staticmethod
    def fetch_one(**kw):
        if 'amazon_category' in kw:
            try:
                return AToECategoryMap.objects.get(amazon_category=kw['amazon_category'])
            except MultipleObjectsReturned as e:
                logger.error("[AMZCAT:%s] Multile category map exist" % kw['amazon_category'])
                return None
            except AToECategoryMap.DoesNotExist as e:
                logger.warning("[AMZCAT:%s] - DoesNotExist: AToECategoryMap matching query does not exist. Create one!" % kw['amazon_category'])
                return None
        elif 'ebay_category_id' in kw:
            try:
                maps = AtoECategoryMapModelManager.fetch(ebay_category_id=kw['ebay_category_id'])
                if maps.count() > 0:
                    return maps.first()
                else:
                    return None
            except Exception as e:
                logger.warning("[ECATID:%s] - Failed to fatch with ebay cagetory id" % kw['ebay_category_id'])
                return None
        else:
            return None

    @staticmethod
    def create(**kw):
        obj = None
        try:
            obj = AToECategoryMap(**kw)
            obj.save()
        except Exception as e:
            logger.error("[Database Error] {e}".format(e=str(e)))
            return False
        return True

    @staticmethod
    def update(cmap, **kw):
        if isinstance(cmap, AToECategoryMap):
            for key, value in kw.iteritems():
                setattr(cmap, key, value)
            cmap.save()
            return True
        return False

    @staticmethod
    def fetch_distinct_ebay_category_info(**kw):
        return AToECategoryMap.objects.filter(**kw).values_list('ebay_category_id', 'ebay_category_name').distinct()


class ExclBrandModelManager(object):

    @staticmethod
    def fetch():
        return ExclBrand.objects.all()

import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'rfi'))

from django.db import connection
from django.core.exceptions import MultipleObjectsReturned

from amazonmws import settings
from amazonmws.loggers import GrayLogger as logger

from rfi_listings.models import EbayItem, EbayItemVariation, EbayItemStat, EbayItemPopularity, EbayCategoryFeatures, EbayStoreCategory


class EbayItemModelManager(object):

    @staticmethod
    def create(ebay_store, asin, ebid, category_id, eb_price, quantity):
        kw = {
            'ebay_store_id': ebay_store.id,
            'asin': asin,
            'ebid': ebid,
            'ebay_category_id': category_id,
            'eb_price': eb_price,
            'quantity': quantity,
            'status': EbayItem.STATUS_ACTIVE,
        }
        return EbayItem.objects.update_or_create(**kw) # (obj, created)

    @staticmethod
    def update_category(ebay_item, ebay_category_id):
        if isinstance(ebay_item, EbayItem):
            ebay_item.ebay_category_id = ebay_category_id
            ebay_item.save()
            return True
        return False

    @staticmethod
    def update_price_and_active(ebay_item, eb_price):
        return EbayItemModelManager.restock(ebay_item=ebay_item, eb_price=eb_price, quantity=settings.EBAY_ITEM_DEFAULT_QUANTITY)

    @staticmethod
    def reduce_quantity(ebay_item, reduce_by=1):
        if isinstance(ebay_item, EbayItem):
            if ebay_item.quantity < 1:
                logger.error("[ASIN:%s|EBID:%s] Unable to reduce quantity - already less than 1" % (ebay_item.asin, ebay_item.ebid))
                return False

            ebay_item.quantity -= reduce_by
            if ebay_item.quantity < 1:
                ebay_item.status = EbayItem.STATUS_OUT_OF_STOCK
            ebay_item.save()
            return True
        return False

    @staticmethod
    def restock(ebay_item, eb_price, quantity):
        if isinstance(ebay_item, EbayItem):
            ebay_item.eb_price = eb_price
            ebay_item.quantity = quantity
            ebay_item.status = EbayItem.STATUS_ACTIVE
            ebay_item.save()
            # log history
            EbayItemRepricedHistoryModelManager.create_with_ebay_item(ebay_item=ebay_item)
            return True
        return False

    @staticmethod
    def oos(ebay_item):
        if isinstance(ebay_item, EbayItem):
            ebay_item.quantity = 0
            ebay_item.status = EbayItem.STATUS_OUT_OF_STOCK
            ebay_item.save()
            # log history
            EbayItemRepricedHistoryModelManager.create_with_ebay_item(ebay_item=ebay_item)
            return True
        return False

    @staticmethod
    def inactive(**kw):
        ebay_item = None
        if 'ebay_item' in kw:
            ebay_item = kw['ebay_item']
        elif 'ebid' in kw:
            try:
                ebay_item = EbayItem.objects.get(ebid=kw['ebid'])
            except MultipleObjectsReturned as e:
                logger.error("[EBID:%s] Multile ebay items exist" % kw['ebid'])
                return False
            except EbayItem.DoesNotExist as e:
                logger.warning("[EBID:%s] No ebay item found" % kw['ebid'])
                return False

        if isinstance(ebay_item, EbayItem):
            ebay_item.quantity = 0
            ebay_item.status = EbayItem.STATUS_INACTIVE
            ebay_item.save()
            # log history
            EbayItemRepricedHistoryModelManager.create_with_ebay_item(ebay_item=ebay_item)
            return True
        return False

    @staticmethod
    def fetch(order=None, desc=False, **kw):
        ebay_items = EbayItem.objects.filter(**kw)
        if order:
            if desc == True:
                ebay_items = ebay_items.order_by('-{}'.format(order))
            else:
                ebay_items = ebay_items.order_by(order)
        return ebay_items

    @staticmethod
    def fetch_one(**kw):
        if 'ebid' in kw:
            try:
                return EbayItem.objects.get(ebid=kw['ebid'])
            except MultipleObjectsReturned as e:
                logger.error("[EBID:%s] Multile ebay items exist" % kw['ebid'])
                return None
            except EbayItem.DoesNotExist as e:
                logger.warning("[EBID:%s] No ebay item found" % kw['ebid'])
                return None

        elif 'ebay_store_id' in kw and 'asin' in kw:
            try:
                return EbayItem.objects.get(
                    ebay_store_id=kw['ebay_store_id'],
                    asin=kw['asin']
                )
            except MultipleObjectsReturned as e:
                logger.error("[EbayStoreID:%d|ASIN:%s] Multile ebay items exist" % (kw['ebay_store_id'], kw['asin']))
                return None
            except EbayItem.DoesNotExist as e:
                logger.warning("[EbayStoreID:%d|ASIN:%s] No ebay item found" % (kw['ebay_store_id'], kw['asin']))
                return None
        else:
            return None

    @staticmethod
    def fetch_distinct_asin(**kw):
        return EbayItemModelManager.fetch_distinct_parent_asins(**kw)

    @staticmethod
    def fetch_distinct_parent_asins(**kw):
        return EbayItem.objects.filter(**kw).values_list('asin', flat=True).distinct()

    @staticmethod
    def is_active(ebay_item):
        if isinstance(ebay_item, EbayItem) and ebay_item.status == EbayItem.STATUS_ACTIVE:
            return True
        return False

    @staticmethod
    def is_inactive(ebay_item):
        if isinstance(ebay_item, EbayItem) and ebay_item.status == EbayItem.STATUS_INACTIVE:
            return True
        return False

    @staticmethod
    def is_oos(ebay_item):
        if isinstance(ebay_item, EbayItem) and ebay_item.status == EbayItem.STATUS_OUT_OF_STOCK:
            return True
        return False

    @staticmethod
    def has_variations(ebay_item):
        variations = EbayItemModelManager.fetch_variations(ebay_item=ebay_item)
        if variations and variations.count() > 0:
            return True
        return False

    @staticmethod
    def fetch_variations(ebay_item):
        variations = EbayItemVariationModelManager.fetch(ebid=ebay_item.ebid)
        if not variations or variations.count() < 1:
            return None
        else:
            return variations

    @staticmethod
    def fetch_variation_skus(ebay_item):
        variations = EbayItemModelManager.fetch_variations(ebay_item)
        if not variations:
            return []
        else:
            return [ v.asin for v in variations ]

    @staticmethod
    def fetch_simpleformat(**kw):
        """ return value: set of sets
            i.e. (
                (1, '282190464028', 'B017S8CXGW'),
                (1, '283290464021', 'B114S7KXYF'),
                (2, '190490464345', 'B643S8KTGA'),
                ...
            )
        """
        return EbayItemVariation.objects.filter(**kw).values_list('ebay_store_id', 'ebid', 'asin').distinct()


class EbayItemVariationModelManager(object):

    @staticmethod
    def create(ebay_item, ebid, asin, specifics, eb_price, quantity):
        kw = {
            'ebay_item_id': ebay_item.id,
            'ebid': ebid,
            'asin': asin,
            'specifics': specifics,
            'eb_price': eb_price,
            'quantity': quantity,
        }
        obj, created = EbayItemVariation.objects.update_or_create(**kw)
        return created

    @staticmethod
    def fetch(**kw):
        return EbayItemVariation.objects.filter(**kw)

    @staticmethod
    def fetch_simpleformat(**kw):
        """ return value: set of sets
            i.e. (
                ('282190464028', 34, 'B017S8CXGW'),
                ('283290464021', 35, 'B114S7KXYF'),
                ('190490464345', 36, 'B643S8KTGA'),
                ...
            )
        """
        return EbayItemVariation.objects.filter(**kw).values_list('ebid', 'id', 'asin').distinct()


    @staticmethod
    def fetch_one(**kw):
        if 'ebid' in kw and 'asin' in kw:
            try:
                return EbayItemVariation.objects.get(
                    ebid=kw['ebid'],
                    asin=kw['asin'])
            except MultipleObjectsReturned as e:
                logger.error("[EBID:%s|ASIN:%s] Multile ebay item variations exist" % (kw['ebid'], kw['asin']))
                return None
            except EbayItemVariation.DoesNotExist as e:
                logger.warning("[EBID:%s|ASIN:%s] No ebay item variation found" % (kw['ebid'], kw['asin']))
                return None
        else:
            return None

    @staticmethod
    def update(variation, **kw):
        if isinstance(variation, EbayItemVariation):
            for key, value in kw.iteritems():
                setattr(variation, key, value)
            variation.save()
            return True
        return False

    @staticmethod
    def update_price_and_active(variation, **kw):
        result = EbayItemVariationModelManager.update(variation, **kw)
        if result:
            # log history
            EbayItemRepricedHistoryModelManager.create_with_ebay_item_variation(variation=variation)
            return True
        else:
            return False

    @staticmethod
    def delete(**kw):
        if 'ebid' in kw and 'asin__in' in kw:
            EbayItemVariation.objects.filter(**kw).delete()
            return True
        return False

    @staticmethod
    def oos(variation):
        if isinstance(variation, EbayItemVariation):
            variation.quantity = 0
            variation.save()
            # log history
            EbayItemRepricedHistoryModelManager.create_with_ebay_item_variation(variation=variation)
            return True
        return False


class EbayItemStatModelManager(object):

    @staticmethod
    def create(ebay_store, ebid, clicks, watches, solds):
        kw = {
            'ebay_store_id': ebay_store.id,
            'ebid': ebid,
            'clicks': clicks,
            'watches': watches,
            'solds': solds,
        }
        obj, created = EbayItemStat.objects.update_or_create(**kw)
        return created

    @staticmethod
    def fetch(**kw):
        return EbayItemStat.objects.filter(**kw)

    @staticmethod
    def fetch_performances_past_days(ebay_store_id, days, order_by='clicks', desc=True, ignore_new_items=False):
        """ return: a set of sets:
                (id,
                ebid,
                curr_clicks,
                curr_watches,
                curr_solds,
                past_clicks,
                past_watches,
                past_solds,
                diff_clicks,
                diff_watches,
                diff_solds,
                new_entry)
        """
        ret = ()

        new_entry_interval = 7 # check item is order than 7 days

        if order_by == 'watches':
            order_by = 'diff_watches'
        elif order_by == 'solds':
            order_by = 'diff_solds'
        else:
            order_by = 'diff_clicks'

        if desc:
            desc = 'DESC'
        else:
            desc = 'ASC'
        if ignore_new_items:
            ignore_new_items = "AND DATE(created_at) < DATE_SUB(CURDATE(), INTERVAL {} DAY)".format(new_entry_interval)
        else:
            ignore_new_items = ""


        query = """SELECT 
    MAX(id) as id,
    ebid,
    MAX(clicks) as curr_clicks,
    MAX(watches) as curr_watches,
    MAX(solds) as curr_solds,
    MAX(IF(DATE(created_at) <= DATE_SUB(CURDATE(), INTERVAL {days} DAY), clicks, 0)) as past_clicks, 
    MAX(IF(DATE(created_at) <= DATE_SUB(CURDATE(), INTERVAL {days} DAY), watches, 0)) as past_watches, 
    MAX(IF(DATE(created_at) <= DATE_SUB(CURDATE(), INTERVAL {days} DAY), solds, 0)) as past_solds,
    MAX(clicks) - MAX(IF(DATE(created_at) <= DATE_SUB(CURDATE(), INTERVAL {days} DAY), clicks, 0)) as diff_clicks,
    MAX(watches) - MAX(IF(DATE(created_at) <= DATE_SUB(CURDATE(), INTERVAL {days} DAY), watches, 0)) as diff_watches,
    MAX(solds) - MAX(IF(DATE(created_at) <= DATE_SUB(CURDATE(), INTERVAL {days} DAY), solds, 0)) as diff_solds,
    IF(DATE(MIN(created_at)) > DATE_SUB(CURDATE(), INTERVAL {new_entry_interval} DAY), 1, 0) as new_entry
FROM ebay_item_stats
    WHERE ebay_store_id = {ebay_store_id} {ignore_new_items}
    GROUP BY ebid ORDER BY {order_by} {desc}""".format(
            days=days,
            new_entry_interval=new_entry_interval,
            ebay_store_id=ebay_store_id,
            ignore_new_items=ignore_new_items,
            order_by=order_by,
            desc=desc)

        with connection.cursor() as cursor:
            cursor.execute(query);
            ret = cursor.fetchall()
        return ret


class EbayItemPopularityModelManager(object):

    @staticmethod
    def create(ebay_store, ebid, popularity=EbayItemPopularity.POPULARITY_NORMAL):
        kw = {
            'ebay_store_id': ebay_store.id,
            'ebid': ebid,
            'popularity': popularity,
        }
        obj, created = EbayItemPopularity.objects.update_or_create(**kw)
        return created

    @staticmethod
    def update(pop, **kw):
        if isinstance(pop, EbayItemPopularityModelManager):
            for key, value in kw.iteritems():
                setattr(pop, key, value)
            pop.save()
            return True
        return False

    @staticmethod
    def fetch(**kw):
        return EbayItemPopularity.objects.filter(**kw)

    @staticmethod
    def fetch_distinct_ebids(**kw):
        return EbayItemPopularity.objects.filter(**kw).values_list('ebid', flat=True).distinct()

    @staticmethod
    def fetch_one(**kw):
        if 'ebid' in kw:
            try:
                return EbayItemPopularity.objects.get(ebid=kw['ebid'])
            except MultipleObjectsReturned as e:
                logger.error("[EBID:%s] Multile ebay item popularities exist" % kw['ebid'])
                return None
            except EbayItemPopularity.DoesNotExist as e:
                logger.warning("[EBID:%s] No ebay item popularity found" % kw['ebid'])
                return None
        else:
            return None

    @staticmethod
    def gc():
        """remove any inactive/removed ebay items (ebids)
        """
        popularities = EbayItemPopularityModelManager.fetch()
        for p in popularities:
            ebay_item = EbayItemModelManager.fetch_one(ebid=p.ebid)
            if not ebay_item or EbayItemModelManager.is_inactive(ebay_item):
                p.delete()
        return True


class EbayItemRepricedHistoryModelManager(object):

    @staticmethod
    def create(ebay_store, ebid, ebay_item_variation_id=None, asin=None, parent_asin=None, price=0.00, quantity=None):
        kw = {
            'ebay_store_id': ebay_store.id,
            'ebid': ebid,
            'ebay_item_variation_id': ebay_item_variation_id,
            'asin': asin,
            'parent_asin': parent_asin,
            'price': price,
            'quantity': quantity,
        }
        obj, created = EbayItemRepricedHistory.objects.update_or_create(**kw)
        return created

    @staticmethod
    def create_with_ebay_item(ebay_item):
        return EbayItemRepricedHistoryModelManager.create(
                ebay_store=ebay_item.ebay_store,
                ebid=ebay_item.ebid,
                ebay_item_variation_id=None,
                asin=None,
                parent_asin=ebay_item.asin,
                price=ebay_item.eb_price,
                quantity=ebay_item.quantity)

    @staticmethod
    def create_with_ebay_item_variation(variation):
        return EbayItemRepricedHistoryModelManager.create(
                ebay_store=variation.ebay_item.ebay_store,
                ebid=variation.ebid,
                ebay_item_variation_id=variation.id,
                asin=variation.asin,
                parent_asin=variation.ebay_item.asin,
                price=variation.eb_price,
                quantity=variation.quantity)


    @staticmethod
    def fetch(**kw):
        return EbayItemRepricedHistory.objects.filter(**kw)


class EbayCategoryFeaturesModelManager(object):
    @staticmethod
    def create(ebay_category_id, ebay_category_name=None, upc_enabled=None, variations_enabled=False):
        kw = {
            'ebay_category_id': ebay_category_id,
            'ebay_category_name': ebay_category_name,
            'upc_enabled': upc_enabled,
            'variations_enabled': variations_enabled,
        }
        obj, created = EbayCategoryFeatures.objects.update_or_create(**kw)
        return created

    @staticmethod
    def fetch(**kw):
        return EbayCategoryFeatures.objects.filter(**kw)

    @staticmethod
    def fetch_one(**kw):
        if 'ebay_category_id' in kw:
            try:
                return EbayCategoryFeatures.objects.get(ebay_category_id=kw['ebay_category_id'])
            except MultipleObjectsReturned as e:
                logger.error("[CategoryID:%s] Multile ebay category features exist" % kw['ebay_category_id'])
                return None
            except EbayCategoryFeatures.DoesNotExist as e:
                logger.warning("[CategoryID:%s] No ebay category feature found" % kw['ebay_category_id'])
                return None
        elif 'id' in kw:
            try:
                return EbayCategoryFeatures.objects.get(id=kw['id'])
            except MultipleObjectsReturned as e:
                logger.error("[CategoryName:%s] Multile ebay category features exist" % kw['id'])
                return None
            except EbayCategoryFeatures.DoesNotExist as e:
                logger.warning("[CategoryName:%s] No ebay category feature found" % kw['id'])
                return None
        else:
            return None

    @staticmethod
    def variations_enabled(**kw):
        if 'ebay_category_id' in kw:
            features = EbayCategoryFeaturesModelManager.fetch_one(ebay_category_id=kw['ebay_category_id'])
            if features:
                return features.variations_enabled
            else:
                return None
        else:
            return False


class EbayStoreCategoryModelManager(object):

    @staticmethod
    def create(ebay_store, category_id, name, parent_category_id=-999, order=0):
        kw = {
            'ebay_store_id': ebay_store.id,
            'category_id': category_id,
            'parent_category_id': parent_category_id,
            'name': name,
            'order': order,
        }
        obj, created = EbayStoreCategory.objects.update_or_create(**kw)
        return created

    @staticmethod
    def fetch_one(**kw):
        if 'category_id' in kw:
            try:
                return EbayStoreCategory.objects.get(category_id=kw['category_id'])
            except MultipleObjectsReturned as e:
                logger.error("[CategoryID:%s] Multile ebay store categories exist" % kw['category_id'])
                return None
            except EbayStoreCategory.DoesNotExist as e:
                logger.warning("[CategoryID:%s] No ebay store category found" % kw['category_id'])
                return None
        elif 'name' in kw:
            try:
                return EbayStoreCategory.objects.get(name=kw['name'])
            except MultipleObjectsReturned as e:
                logger.error("[CategoryName:%s] Multile ebay store categories exist" % kw['name'])
                return None
            except EbayStoreCategory.DoesNotExist as e:
                logger.warning("[CategoryName:%s] No ebay store category found" % kw['name'])
                return None
        else:
            return None

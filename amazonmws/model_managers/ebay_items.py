import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'rfi'))

from django.db import connection
from django.core.exceptions import MultipleObjectsReturned

from amazonmws import settings
from amazonmws.loggers import GrayLogger as logger

from rfi_listings.models import *


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
    def update(ebay_item, **kw):
        if isinstance(ebay_item, EbayItem):
            for key, value in kw.iteritems():
                setattr(ebay_item, key, value)
            ebay_item.save()
            return True
        return False

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
            return True
        return False

    @staticmethod
    def oos(ebay_item):
        if isinstance(ebay_item, EbayItem):
            ebay_item.quantity = 0
            ebay_item.status = EbayItem.STATUS_OUT_OF_STOCK
            ebay_item.save()
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
            return True
        return False

    @staticmethod
    def delete(delete_vars=True, **kw):
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
            try:
                if delete_vars:
                    EbayItemModelManager.delete_variations(ebay_item=ebay_item)
                ebay_item.delete()
                return True
            except Exception as e:
                logger.error("[EBID:{}] Unable to delete ebay item".format(ebay_item.ebid))
                return False
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
    def delete_variations(ebay_item):
        variations = EbayItemVariationModelManager.fetch(ebid=ebay_item.ebid)
        if not variations or variations.count() < 1:
            return None
        else:
            variations.delete()
            return True

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
        return EbayItem.objects.filter(**kw).values_list('ebay_store_id', 'ebid', 'asin').distinct()

    @staticmethod
    def fetch_distinct_parent_asins_by_popularity(ebay_store_id, popularity):
        ret = []
        if popularity == 2:
            popularity_condition = "(p.popularity = {} OR p.popularity IS NULL)".format(popularity)
        else:
            popularity_condition = "p.popularity = {}".format(popularity)

        query = """SELECT i.asin
        FROM ebay_items i
            LEFT JOIN ebay_item_popularities p on p.ebid = i.ebid
        WHERE i.ebay_store_id = {ebay_store_id} AND i.status <> 0 AND {popularity_condition}""".format(
                ebay_store_id=ebay_store_id,
                popularity=popularity,
                popularity_condition=popularity_condition)

        with connection.cursor() as cursor:
            cursor.execute(query);
            for el in cursor.fetchall():
                ret.append(el[0])
        return ret

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
        return EbayItemVariation.objects.update_or_create(**kw)

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
            return True
        return False


class EbayPictureModelManager(object):

    @staticmethod
    def create(**kw):
        try:
            obj = EbayPicture(**kw)
            obj.save()
            return obj
        except Exception as e:
            logger.error(str(e))
        return None

    @staticmethod
    def update(picture, **kw):
        if isinstance(picture, EbayPicture):
            for key, value in kw.iteritems():
                setattr(picture, key, value)
            picture.save()
            return True
        return False

    @staticmethod
    def delete(picture, delete_members=True):
        if isinstance(picture, EbayPicture):
            if delete_members:
                EbayPictureSetMemberModelManager.fetch(ebay_picture=picture).delete()
            picture.delete()
            return True
        return False

    @staticmethod
    def fetch_one(**kw):
        try:
            return EbayPicture.objects.get(**kw)
        except MultipleObjectsReturned as e:
            logger.error("[{}] Multile picture info exist".format(kw['source_picture_url'] if 'source_picture_url' in kw else kw['picture_url'] if 'picture_url' in kw else ''))
            return None
        except EbayPicture.DoesNotExist as e:
            logger.warning("[{}] - DoesNotExist: EbayPicture matching query does not exist. Create one!".format(kw['source_picture_url'] if 'source_picture_url' in kw else kw['picture_url'] if 'picture_url' in kw else ''))
            return None

    @staticmethod
    def fetch(**kw):
        return EbayPicture.objects.filter(**kw).order_by('id')

    @staticmethod
    def get_ebay_picture_url(source_picture_url):
        pict = EbayPictureModelManager.fetch_one(source_picture_url=source_picture_url)
        if not pict:
            return None
        else:
            return pict.picture_url

    @staticmethod
    def get_ebay_picture_urls(picture_urls):
        ebay_urls = []
        for picture_url in picture_urls:
            ebay_url = EbayPictureModelManager.get_ebay_picture_url(source_picture_url=picture_url)
            if ebay_url:
                ebay_urls.append(ebay_url)
        return ebay_urls


class EbayPictureSetMemberModelManager(object):

    @staticmethod
    def create(**kw):
        try:
            obj = EbayPictureSetMember(**kw)
            obj.save()
            return obj
        except Exception as e:
            logger.error(str(e))
        return None

    @staticmethod
    def update(picture, **kw):
        if isinstance(picture, EbayPictureSetMember):
            for key, value in kw.iteritems():
                setattr(picture, key, value)
            picture.save()
            return True
        return False

    @staticmethod
    def fetch_one(**kw):
        try:
            return EbayPictureSetMember.objects.get(**kw)
        except MultipleObjectsReturned as e:
            logger.error("[{}] Multile picture info exist".format(kw['member_url'] if 'member_url' in kw else 'None'))
            return None
        except EbayPictureSetMember.DoesNotExist as e:
            logger.warning("[{}] - DoesNotExist: EbayPictureSetMember matching query does not exist. Create one!".format(kw['member_url'] if 'member_url' in kw else 'None'))
            return None

    @staticmethod
    def fetch(**kw):
        return EbayPictureSetMember.objects.filter(**kw).order_by('height')


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
    def fetch_performances_past_days(ebay_store_id, days, order_by='clicks', desc=True, days_as_new_item=10):
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

        query = """SELECT
        id, ebid, curr_clicks, curr_watches, curr_solds, past_clicks, past_watches, past_solds, diff_clicks, diff_watches, diff_solds, new_entry, parent_asin, @row := @row + 1 AS row_index
        FROM
            (SELECT
                MAX(s.id) as id,
                s.ebid,
                MAX(s.clicks) as curr_clicks,
                MAX(s.watches) as curr_watches,
                MAX(s.solds) as curr_solds,
                MAX(IF(DATE(s.created_at) <= DATE_SUB(CURDATE(), INTERVAL {days} DAY), s.clicks, 0)) as past_clicks,
                MAX(IF(DATE(s.created_at) <= DATE_SUB(CURDATE(), INTERVAL {days} DAY), s.watches, 0)) as past_watches,
                MAX(IF(DATE(s.created_at) <= DATE_SUB(CURDATE(), INTERVAL {days} DAY), s.solds, 0)) as past_solds,
                MAX(s.clicks) - MAX(IF(DATE(s.created_at) <= DATE_SUB(CURDATE(), INTERVAL {days} DAY), s.clicks, 0)) as diff_clicks,
                MAX(s.watches) - MAX(IF(DATE(s.created_at) <= DATE_SUB(CURDATE(), INTERVAL {days} DAY), s.watches, 0)) as diff_watches,
                MAX(s.solds) - MAX(IF(DATE(s.created_at) <= DATE_SUB(CURDATE(), INTERVAL {days} DAY), s.solds, 0)) as diff_solds,
                IF(DATE(MIN(s.created_at)) > DATE_SUB(CURDATE(), INTERVAL {days_as_new_item} DAY), 1, 0) as new_entry,
                i.asin as parent_asin
            FROM ebay_item_stats s
                LEFT JOIN ebay_items i on i.ebid = s.ebid
                WHERE s.ebay_store_id = {ebay_store_id} AND i.status <> 0
                GROUP BY s.ebid ORDER BY {order_by} {desc}) r
        CROSS JOIN (SELECT @row := 0) rr""".format(
            days=days,
            days_as_new_item=days_as_new_item,
            ebay_store_id=ebay_store_id,
            order_by=order_by,
            desc=desc)

        with connection.cursor() as cursor:
            cursor.execute(query);
            ret = cursor.fetchall()
        return ret


class EbayItemPopularityModelManager(object):

    @staticmethod
    def create(**kw):
        try:
            if 'popularity' not in kw:
                kw['popularity'] = EbayItemPopularity.POPULARITY_NORMAL
            obj = EbayItemPopularity(**kw)
            obj.save()
            return obj
        except Exception as e:
            logger.error(str(e))
        return None

    @staticmethod
    def update(pop, **kw):
        if isinstance(pop, EbayItemPopularity):
            for key, value in kw.iteritems():
                setattr(pop, key, value)
            pop.save()
            return True
        return False

    @staticmethod
    def fetch(**kw):
        return EbayItemPopularity.objects.filter(**kw)

    @staticmethod
    def fetch_distinct_parent_asins(**kw):
        return EbayItemPopularity.objects.filter(**kw).values_list('parent_asin', flat=True).distinct()

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
        popularities = EbayItemPopularityModelManager.fetch()
        for p in popularities:
            if not p.parent_asin:
                """remove element doesn't have parent_asin value
                """
                p.delete()
                continue
            ebay_item = EbayItemModelManager.fetch_one(ebid=p.ebid)
            if not ebay_item or EbayItemModelManager.is_inactive(ebay_item):
                """remove any inactive/removed ebay items (ebids)
                """
                p.delete()
        return True


class EbayItemLastReviseAttemptedModelManager(object):

    @staticmethod
    def create(**kw):
        try:
            obj = EbayItemLastReviseAttempted(**kw)
            obj.save()
        except Exception as e:
            logger.error(str(e))
            return False
        return True

    @staticmethod
    def fetch_one(**kw):
        ebay_item_variation_id = 0
        if 'ebay_item_variation_id' in kw:
            ebay_item_variation_id = kw['ebay_item_variation_id']
        if 'ebid' in kw:
            try:
                return EbayItemLastReviseAttempted.objects.get(ebid=kw['ebid'],
                    ebay_item_variation_id=ebay_item_variation_id)
            except MultipleObjectsReturned as e:
                logger.error("[EBID:{}|VariationID:{}] Multile EbayItemLastReviseAttempted objs exist".format(kw['ebid'], ebay_item_variation_id ))
                return None
            except EbayItemLastReviseAttempted.DoesNotExist as e:
                logger.error("[EBID:{}|VariationID:{}] No EbayItemLastReviseAttempted found".format(kw['ebid'], ebay_item_variation_id ))
                return None
        else:
            return None

    @staticmethod
    def update(revise_attempted):
        if isinstance(revise_attempted, EbayItemLastReviseAttempted):
            # db, updated_at field should be updated
            revise_attempted.save()
            return True
        return False


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
    def update(feature, **kw):
        if isinstance(feature, EbayCategoryFeatures):
            for key, value in kw.iteritems():
                setattr(feature, key, value)
            feature.save()
            return True
        return False

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
    def create(ebay_store, category_id, name, parent_category_id=-999, order=0, level=1):
        try:
            kw = {
                'ebay_store_id': ebay_store.id,
                'category_id': category_id,
                'parent_category_id': parent_category_id,
                'name': name,
                'order': order,
                'level': level,
            }
            obj = EbayStoreCategory(**kw)
            obj.save()
        except Exception as e:
            logger.error(str(e))
            return None
        return obj

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
        elif 'name' in kw and 'parent_category_id' in kw and 'ebay_store_id' in kw:
            try:
                return EbayStoreCategory.objects.get(name=kw['name'],
                    parent_category_id=kw['parent_category_id'],
                    ebay_store_id=kw['ebay_store_id'])
            except MultipleObjectsReturned as e:
                logger.error("[CategoryName:%s] Multile ebay store categories exist" % kw['name'])
                return None
            except EbayStoreCategory.DoesNotExist as e:
                logger.warning("[CategoryName:%s] No ebay store category found" % kw['name'])
                return None
        else:
            return None

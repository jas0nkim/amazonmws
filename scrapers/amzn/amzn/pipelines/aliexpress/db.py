import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..'))

import datetime
import json

from scrapy.exceptions import DropItem

from amazonmws import django_cli
django_cli.execute()

from amazonmws import utils as amazonmws_utils
from amazonmws.model_managers.aliexpress_stores import *
from amazonmws.model_managers.aliexpress_items import *
from amazonmws.model_managers.ebay_stores import *

from amzn.spiders import *
from amzn.items import AliexpressItem as ScrapyAliexpressItem, AliexpressItemDescription as ScrapyAliexpressItemDescription, AliexpressItemSizeInfo as ScrapyAliexpressItemSizeInfo, AliexpressItemShipping as ScrapyAliexpressItemShipping, AliexpressStoreItem as ScrapyAliexpressStoreItem, AliexpressStoreItemFeedback as ScrapyAliexpressStoreItemFeedback, AliexpressStoreItemFeedbackDetailed as ScrapyAliexpressStoreItemFeedbackDetailed


class AliexpressStoreCachePipeline(object):

    def __cache_aliexpress_store(self, item, spider):
        aliexpress_store = AliexpressStoreModelManager.fetch_one(store_id=item.get('store_id'))
        if aliexpress_store == None: # create
            if not item.get('status'): # do nothing
                # do not create new entry for any invalid data (i.e. 404 pages)
                return False
            AliexpressStoreModelManager.create(store_id=item.get('store_id'),
                store_name=item.get('store_name', None),
                company_id=item.get('company_id', None),
                owner_member_id=item.get('owner_member_id', None),
                store_location=item.get('store_location', None),
                store_opened_since=datetime.datetime.strptime(item.get('store_opened_since'), '%b %d, %Y').date() if item.get('store_opened_since', None) else None,
                is_topratedseller=item.get('is_topratedseller', False),
                deliveryguarantee_days=item.get('deliveryguarantee_days', None),
                return_policy=item.get('return_policy', None),
                has_buyerprotection=item.get('has_buyerprotection', True),
                status=item.get('status'))
        else: # update
            if not item.get('status'):
                AliexpressStoreModelManager.inactive(aliexpress_store)
                return True
            AliexpressStoreModelManager.update(aliexpress_store,
                store_name=item.get('store_name', None),
                company_id=item.get('company_id', None),
                owner_member_id=item.get('owner_member_id', None),
                store_location=item.get('store_location', None),
                store_opened_since=datetime.datetime.strptime(item.get('store_opened_since'), '%b %d, %Y').date() if item.get('store_opened_since', None) else None,
                is_topratedseller=item.get('is_topratedseller', False),
                deliveryguarantee_days=item.get('deliveryguarantee_days', None),
                return_policy=item.get('return_policy', None),
                has_buyerprotection=item.get('has_buyerprotection', True),
                status=item.get('status'))
        return True

    def __cache_aliexpress_store_feedback(self, item, spider):
        alx_store_feedback = AliexpressStoreFeedbackModelManager.fetch_one(store_id=item.get('store_id'))
        if alx_store_feedback == None: # create
            AliexpressStoreFeedbackModelManager.create(store_id=item.get('store_id'),
                feedback_score=item.get('feedback_score', 0),
                feedback_percentage=item.get('feedback_percentage', 0))
        else: # update
            AliexpressStoreFeedbackModelManager.update(alx_store_feedback,
                feedback_score=item.get('feedback_score', 0),
                feedback_percentage=item.get('feedback_percentage', 0))
        return True

    def __cache_aliexpress_store_feedback_detailed(self, item, spider):
        alx_store_feedback_detailed = AliexpressStoreFeedbackDetailedModelManager.fetch_one(store_id=item.get('store_id'))
        if alx_store_feedback_detailed == None: # create
            AliexpressStoreFeedbackDetailedModelManager.create(store_id=item.get('store_id'),
                itemasdescribed_score=item.get('itemasdescribed_score', 0),
                itemasdescribed_ratings=item.get('itemasdescribed_ratings', 0),
                itemasdescribed_percent=item.get('itemasdescribed_percent', 0),
                communication_score=item.get('communication_score', 0),
                communication_ratings=item.get('communication_ratings', 0),
                communication_percent=item.get('communication_percent', 0),
                shippingspeed_score=item.get('shippingspeed_score', 0),
                shippingspeed_ratings=item.get('shippingspeed_ratings', 0),
                shippingspeed_percent=item.get('shippingspeed_percent', 0))
        else: # update
            AliexpressStoreFeedbackDetailedModelManager.update(alx_store_feedback_detailed,
                itemasdescribed_score=item.get('itemasdescribed_score', 0),
                itemasdescribed_ratings=item.get('itemasdescribed_ratings', 0),
                itemasdescribed_percent=item.get('itemasdescribed_percent', 0),
                communication_score=item.get('communication_score', 0),
                communication_ratings=item.get('communication_ratings', 0),
                communication_percent=item.get('communication_percent', 0),
                shippingspeed_score=item.get('shippingspeed_score', 0),
                shippingspeed_ratings=item.get('shippingspeed_ratings', 0),
                shippingspeed_percent=item.get('shippingspeed_percent', 0))
        return True

    def process_item(self, item, spider):
        if isinstance(item, ScrapyAliexpressStoreItem): # AliexpressStoreItem (scrapy item)
            self.__cache_aliexpress_store(item, spider)
        elif isinstance(item, ScrapyAliexpressStoreItemFeedback): # AliexpressStoreItemFeedback (scrapy item)
            self.__cache_aliexpress_store_feedback(item, spider)
        elif isinstance(item, ScrapyAliexpressStoreItemFeedbackDetailed): # AliexpressStoreItemFeedbackDetailed (scrapy item)
            self.__cache_aliexpress_store_feedback_detailed(item, spider)
        return item


class AliexpressItemCachePipeline(object):

    def __cache_aliexpress_category(self, item, spider):
        ret = {
            'category_id': None,
            'category_name': None,
            'category': None,
        }
        ret['category'] = item.get('_category_route', {}).get('category', None)
        _cat_route = item.get('_category_route', {}).get('route', [])
        i = 1
        while len(_cat_route) > i:
            alx_cat = AliexpressCategoryModelManager.fetch_one(category_id=_cat_route[i].get('id'))
            if alx_cat == None: # create item
                AliexpressCategoryModelManager.create(category_id=_cat_route[i].get('id'),
                    category_name=_cat_route[i].get('name'),
                    parent_category_id=_cat_route[i-1].get('id'),
                    parent_category_name=_cat_route[i-1].get('name'),
                    root_category_id=_cat_route[0].get('id'),
                    root_category_name=_cat_route[0].get('name'),
                    is_leaf=_cat_route[i].get('is_leaf'))            
            if _cat_route[i].get('is_leaf'):
                ret['category_id'] = _cat_route[i].get('id')
                ret['category_name'] = _cat_route[i].get('name')
            i += 1
        return ret

    def __cache_aliexpress_item(self, item, spider):
        _cat_info = self.__cache_aliexpress_category(item, spider)

        aliexpress_item = AliexpressItemModelManager.fetch_one(alxid=item.get('alxid'))
        if aliexpress_item == None: # create item
            if not item.get('status'): # do nothing
                # do not create new entry for any invalid data (i.e. 404 pages)
                return False
            AliexpressItemModelManager.create(alxid=item.get('alxid'),
                url=item.get('url'),
                store_id=item.get('store_id', None),
                store_name=item.get('store_name', None),
                store_location=item.get('store_location', None),
                store_opened_since=datetime.datetime.strptime(item.get('store_openedsince'), '%b %d, %Y').date() if item.get('store_openedsince', None) else None,
                category_id=_cat_info.get('category_id'),
                category_name=_cat_info.get('category_name'),
                category=_cat_info.get('category'),
                title=item.get('title'),
                market_price=amazonmws_utils.number_to_dcmlprice(item.get('market_price', 0)),
                price=amazonmws_utils.number_to_dcmlprice(item.get('price')),
                quantity=item.get('quantity', None),
                specifications=item.get('specifications', None), # json string
                pictures=item.get('pictures', None), # json string (list of picture urls)
                review_count=item.get('review_count', 0),
                review_rating=item.get('review_rating', 0),
                orders=item.get('orders'),
                status=item.get('status'))
        else: # update item
            if not item.get('status'):
                AliexpressItemModelManager.inactive(aliexpress_item)
                return True
            AliexpressItemModelManager.update(aliexpress_item,
                url=item.get('url'),
                store_id=item.get('store_id', None),
                store_name=item.get('store_name', None),
                store_location=item.get('store_location', None),
                store_opened_since=datetime.datetime.strptime(item.get('store_openedsince'), '%b %d, %Y').date() if item.get('store_openedsince', None) else None,
                category_id=item.get(''),
                category_name=item.get(''),
                category=item.get(''),
                title=item.get('title'),
                market_price=amazonmws_utils.number_to_dcmlprice(item.get('market_price', 0)),
                price=amazonmws_utils.number_to_dcmlprice(item.get('price')),
                quantity=item.get('quantity', None),
                specifications=item.get('specifications', None), # json string
                pictures=item.get('pictures', None), # json string (list of picture urls)
                review_count=item.get('review_count', 0),
                review_rating=item.get('review_rating', 0),
                orders=item.get('orders'),
                status=item.get('status'))
        return True

    def __cache_aliexpress_item_sku(self, alxid, data, spider):
        alx_item_sku = AliexpressItemSkuModelManager.fetch_one(alxid=alxid, sku=data.get('skuPropIds'))
        _sku_val = data.get('skuVal', None)
        if alx_item_sku == None: # create item
            if not _sku_val:
                return False
            AliexpressItemSkuModelManager.create(alxid=alxid,
                sku=data.get('skuPropIds'),
                market_price=amazonmws_utils.number_to_dcmlprice(_sku_val.get('skuPrice', 0)),
                price=amazonmws_utils.number_to_dcmlprice(_sku_val.get('actSkuPrice') if 'actSkuPrice' in _sku_val else _sku_val.get('skuPrice', 0)),
                quantity=_sku_val.get('inventory', None),
                specifications=json.dumps(data.get('skuSpec', {})),
                pictures=json.dumps(data.get('skuPics', [])),
                bulk_price=amazonmws_utils.number_to_dcmlprice(_sku_val.get('actSkuBulkPrice') if 'actSkuBulkPrice' in _sku_val else _sku_val.get('skuBulkPrice', 0)),
                bulk_order=_sku_val.get('bulkOrder', None),
                raw_data=json.dumps(data),
                status=True)
        else: # update item
            if not _sku_val:
                AliexpressItemSkuModelManager.inactive(alx_item_sku)
                return True
            AliexpressItemSkuModelManager.update(item_sku=alx_item_sku,
                market_price=amazonmws_utils.number_to_dcmlprice(_sku_val.get('skuPrice', 0)),
                price=amazonmws_utils.number_to_dcmlprice(_sku_val.get('actSkuPrice') if 'actSkuPrice' in _sku_val else _sku_val.get('skuPrice', 0)),
                quantity=_sku_val.get('inventory', None),
                specifications=json.dumps(data.get('skuSpec', {})),
                pictures=json.dumps(data.get('skuPics', [])),
                bulk_price=amazonmws_utils.number_to_dcmlprice(_sku_val.get('actSkuBulkPrice') if 'actSkuBulkPrice' in _sku_val else _sku_val.get('skuBulkPrice', 0)),
                bulk_order=_sku_val.get('bulkOrder', None),
                raw_data=json.dumps(data),
                status=True)
        return True

    def __cache_aliexpress_item_description(self, item):
        alx_item_desc = AliexpressItemDescriptionModelManager.fetch_one(alxid=item.get('alxid'))
        if alx_item_desc == None: # create item
            AliexpressItemDescriptionModelManager.create(alxid=item.get('alxid'),
                description=item.get('description', None))
        else: # update item
            AliexpressItemDescriptionModelManager.update(alx_item_desc,
                description=item.get('description', None))
        return True

    def __cache_aliexpress_item_size_info(self, item):
        alx_item_apparel = AliexpressItemApparelModelManager.fetch_one(alxid=item.get('alxid'))
        if alx_item_apparel == None: # create item
            AliexpressItemApparelModelManager.create(alxid=item.get('alxid'),
                size_chart=json.dumps(item.get('_size_data')) if item.get('_size_data', {}) else None)
        else: # update item
            AliexpressItemApparelModelManager.update(item_apparel=alx_item_apparel,
                size_chart=json.dumps(item.get('_size_data')) if item.get('_size_data', {}) else None)
        return True

    def __get_epacket_info(self, shippings):
        ret = {
            'has_epacket': False,
            'epacket_cost': 0,
            'epacket_estimated_delivery_time_min': 0,
            'epacket_estimated_delivery_time_max': 0,
            'epacket_tracking': False,
        }
        for shipping_info in shippings:
            if 'companyDisplayName' in shipping_info and shipping_info['companyDisplayName'] == 'ePacket':
                ret['has_epacket'] = True
                ret['epacket_cost'] = amazonmws_utils.number_to_dcmlprice(shipping_info['price'])
                ret['epacket_estimated_delivery_time_min'] = int(shipping_info['time'].split('-')[0])
                ret['epacket_estimated_delivery_time_min'] = int(shipping_info['time'].split('-')[1])
                ret['epacket_tracking'] = shipping_info['isTracked']
                return ret
            else:
                continue
        return ret

    def __cache_aliexpress_item_shipping(self, item):
        alx_item_shipping = AliexpressItemShippingModelManager.fetch_one(alxid=item.get('alxid'), country_code=item.get('country_code'))
        _epacket_info = self.__get_epacket_info(shippings=item.get('_shippings', {}).get('freight', []) if item.get('_shippings', {}) else [])
        if alx_item_shipping == None: # create item
            AliexpressItemShippingModelManager.create(alxid=item.get('alxid'),
                country_code=item.get('country_code'),
                has_epacket=_epacket_info.get('has_epacket', False),
                epacket_cost=_epacket_info.get('has_epacket', False),
                epacket_estimated_delivery_time_min=_epacket_info.get('has_epacket', False),
                epacket_estimated_delivery_time_max=_epacket_info.get('has_epacket', False),
                epacket_tracking=_epacket_info.get('has_epacket', False),
                all_options=json.dumps(item.get('_shippings')) if item.get('_shippings', {}) else None,
                status=True)
        else: # update item
            AliexpressItemShippingModelManager.update(item_shipping=alx_item_shipping,
                has_epacket=_epacket_info.get('has_epacket', False),
                epacket_cost=_epacket_info.get('has_epacket', False),
                epacket_estimated_delivery_time_min=_epacket_info.get('has_epacket', False),
                epacket_estimated_delivery_time_max=_epacket_info.get('has_epacket', False),
                epacket_tracking=_epacket_info.get('has_epacket', False),
                all_options=json.dumps(item.get('_shippings')) if item.get('_shippings', {}) else None,
                status=True)
        return True

    def process_item(self, item, spider):
        if isinstance(item, ScrapyAliexpressItem): # AliexpressItem (scrapy item)
            # if item.get('_cached', False):
            #     logger.info("[ASIN:{}] _cached - no database saving".format(item.get('asin')))
            #     # this item is cached. do not save into db
            #     return item
            # if not self.__is_valid_item(item):
            #     item['status'] = False
            self.__cache_aliexpress_item(item, spider)
            _skus = item.get('_skus', [])
            if len(_skus) > 0:
                for _sku_data in _skus:
                    self.__cache_aliexpress_item_sku(alxid=item.get('alxid', ''), data=_sku_data, spider=spider)
        elif isinstance(item, ScrapyAliexpressItemDescription): # AliexpressItemDescription (scrapy item)
            self.__cache_aliexpress_item_description(item)
        elif isinstance(item, ScrapyAliexpressItemSizeInfo): # AliexpressItemSizeInfo (scrapy item)
            self.__cache_aliexpress_item_size_info(item)
        elif isinstance(item, ScrapyAliexpressItemShipping): # AliexpressItemShipping (scrapy item)
            self.__cache_aliexpress_item_shipping(item)
        return item


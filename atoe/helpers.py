import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'scrapers', 'amzn'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'rfi'))

import datetime
import json
from django.utils import timezone

from amazonmws import settings as amazonmws_settings, utils as amazonmws_utils
from amazonmws.loggers import GrayLogger as logger, StaticFieldFilter, get_logger_name
from amazonmws.model_managers import *
from amazonmws.errors import record_ebay_category_error, GetOutOfLoop

from atoe.actions import EbayItemAction, EbayItemCategoryAction, EbayOrderAction, EbayStoreCategoryAction

from rfi_sources.models import AmazonItem


class ListingHandler(object):

    ebay_store = None
    # max_num_listing = None
    
    __min_review_count = None
    __asins_exclude = []

    # 
    # amazon to ebay category mapping dictionary
    #
    # e.g. {'Cell Phones & Accessories : Accessories : Car Accessories : Car Cradles & Mounts': 35190,
    #   'Electronics : Car & Vehicle Electronics : Marine Electronics : Marine GPS Accessories': 39754,
    #   'Automotive : Interior Accessories : Consoles & Organizers : Dash-Mounted Holders': 33695,
    #   ...
    #   }
    __atemap = {}
    __excl_brands = None

    __disallowed_category_keywords = [
        'knives',
        'knife',
        'blades',
        'blade',
    ]

    def __init__(self, ebay_store, **kwargs):
        self.ebay_store = ebay_store
        if 'min_review_count' in kwargs:
            self.__min_review_count = kwargs['min_review_count']
        if 'asins_exclude' in kwargs:
            self.__asins_exclude = kwargs['asins_exclude']
        
        cmap = AtoECategoryMapModelManager.fetch()
        self.__atemap = { m.amazon_category:m.ebay_category_id for m in cmap }
        self.__excl_brands = ExclBrandModelManager.fetch()
        logger.addFilter(StaticFieldFilter(get_logger_name(), 'atoe_listing'))

    def __restock(self, amazon_item, ebay_item):
        succeed = False
        maxed_out = False

        action = EbayItemAction(ebay_store=self.ebay_store,
                    ebay_item=ebay_item)
        eb_price = amazonmws_utils.calculate_profitable_price(amazon_item.price, self.ebay_store)
        if eb_price <= 0:
            logger.error("[%s|ASIN:%s] No listing price available" % (self.ebay_store.username, amazon_item.asin))
            return (succeed, maxed_out)
        succeed = action.revise_inventory(eb_price, amazonmws_settings.EBAY_ITEM_DEFAULT_QUANTITY)
        maxed_out = action.maxed_out()
        if succeed:
            # store in database
            EbayItemModelManager.restock(ebay_item, eb_price, amazonmws_settings.EBAY_ITEM_DEFAULT_QUANTITY)
        return (succeed, maxed_out)

    def __oos(self, amazon_item, ebay_item):
        try:
            ebay_action = EbayItemAction(ebay_store=self.ebay_store, ebay_item=ebay_item, amazon_item=amazon_item)
            succeed = ebay_action.revise_inventory(eb_price=None, quantity=0, do_revise_item=False)
            if succeed:
                EbayItemModelManager.oos(ebay_item)
            return (succeed, False)
        except Exception:
            return (False, False)

    def __list_new(self, amazon_item):
        succeed = False
        maxed_out = False

        if amazon_item.category and any(x in amazon_item.category.lower() for x in self.__disallowed_category_keywords):
            logger.error("[%s] Knives/Blades are not allowed to list - %s" % (self.ebay_store.username, amazon_item.category))
            return (False, False)

        if amazon_item.category in self.__atemap:
            category_id = self.__atemap[amazon_item.category]
        else:
            category_id = self.__find_ebay_category_id(amazon_item.title)
        
        if not category_id:
            logger.error("[%s] No category id found in map data - %s" % (self.ebay_store.username, amazon_item.category))
            record_ebay_category_error(
                '', 
                amazon_item.asin,
                amazon_item.category,
                None,
                '',
            )
            return (False, False)

        action = EbayItemAction(ebay_store=self.ebay_store, amazon_item=amazon_item)
        eb_price = amazonmws_utils.calculate_profitable_price(amazon_item.price, self.ebay_store)
        if eb_price <= 0:
            logger.error("[%s|ASIN:%s] No listing price available" % (self.ebay_store.username, amazon_item.asin))
            return (succeed, maxed_out)

        picture_urls = action.upload_pictures(AmazonItemPictureModelManager.fetch(asin=amazon_item.asin))
        if len(picture_urls) < 1:
            logger.error("[%s|ASIN:%s] No item pictures available" % (self.ebay_store.username, amazon_item.asin))
            return (succeed, maxed_out)

        store_category_id, store_category_name = self.__find_ebay_store_category_info(amazon_category=amazon_item.category)
        ebid = action.add_item(category_id=category_id, 
                            picture_urls=picture_urls, 
                            eb_price=eb_price, 
                            quantity=amazonmws_settings.EBAY_ITEM_DEFAULT_QUANTITY,
                            store_category_id=store_category_id)
        maxed_out = action.maxed_out()
        if ebid:
            # store in database
            obj, created = EbayItemModelManager.create(ebay_store=self.ebay_store, 
                                    asin=amazon_item.parent_asin, 
                                    ebid=ebid, 
                                    category_id=category_id, 
                                    eb_price=eb_price, 
                                    quantity=amazonmws_settings.EBAY_ITEM_DEFAULT_QUANTITY)
            if obj:
                succeed = True
        return (succeed, maxed_out)

    def __list_new_v(self, amazon_items):
        succeed = False
        maxed_out = False
        
        amazon_item = amazon_items.first()
        if amazon_item.category and any(x in amazon_item.category.lower() for x in self.__disallowed_category_keywords):
            logger.error("[%s] Knives/Blades are not allowed to list - %s" % (self.ebay_store.username, amazon_item.category))
            return (False, False)

        if amazon_item.category in self.__atemap:
            category_id = self.__atemap[amazon_item.category]
        else:
            category_id = self.__find_ebay_category_id(amazon_item.title)
        
        if not category_id:
            logger.error("[%s] No category id found in map data - %s" % (self.ebay_store.username, amazon_item.category))
            record_ebay_category_error(
                '', 
                amazon_item.asin,
                amazon_item.category,
                None,
                '',
            )
            return (False, False)

        action = EbayItemAction(ebay_store=self.ebay_store, amazon_item=amazon_item)
        common_pictures = self.__get_variations_common_pictures(amazon_items=amazon_items)
        variations = self.__build_variations_obj(amazon_items=amazon_items, common_pictures=common_pictures)
        store_category_id, store_category_name = self.__find_ebay_store_category_info(amazon_category=amazon_item.category)
        ebid = action.add_item(category_id=category_id,
                        picture_urls=common_pictures, 
                        eb_price=None, 
                        quantity=None,
                        title=self.__build_variations_common_title(amazon_items=amazon_items),
                        store_category_id=store_category_id,
                        variations=variations)
        maxed_out = action.maxed_out()
        if ebid:
            # store in database
            obj, created = EbayItemModelManager.create(ebay_store=self.ebay_store, 
                                    asin=amazon_item.parent_asin, 
                                    ebid=ebid, 
                                    category_id=category_id, 
                                    eb_price=variations['Variation'][0]['StartPrice'], # 1st variation's price
                                    quantity=None)
            if obj:
                for v in variations['Variation']:
                    a = AmazonItemModelManager.fetch_one(asin=v['SKU'])
                    if a is None:
                        continue
                    EbayItemVariationModelManager.create(ebay_item=obj,
                                                    ebid=ebid,
                                                    asin=v['SKU'],
                                                    specifics=a.variation_specifics,
                                                    eb_price=v['StartPrice'],
                                                    quantity=v['Quantity'])
                succeed = True
        return (succeed, maxed_out)

    def __aware_brand(self, amazon_item):
        if self.__excl_brands.count() < 1:
            return False
        for excl_brand in self.__excl_brands:
            if amazon_item.brand_name == excl_brand.brand_name:
                if not excl_brand.category: # brand should excluded from all categories
                    logger.warning('[ASIN:%s] reported brand - %s - ignoring...' % (amazon_item.asin, amazon_item.brand_name))
                    return True
                else:
                    if amazon_item.category and amazon_item.category.startswith(excl_brand.category):
                        logger.warning('[ASIN:%s] reported brand - %s - ignoring...' % (amazon_item.asin, amazon_item.brand_name))
                        return True
        return False

    def __find_ebay_category_id(self, title):
        title = amazonmws_utils.to_keywords(title)
        if not title:
            return None
        ebay_action = EbayItemAction(ebay_store=self.ebay_store)
        return ebay_action.find_category_id(title)

    def __find_ebay_store_category_info(self, amazon_category):
        try:
            root_category = [c.strip() for c in amazon_category.split(':')][0]
            ebay_store_category = EbayStoreCategoryModelManager.fetch_one(name=root_category)
            if ebay_store_category:
                return (ebay_store_category.category_id, root_category)
            else:
                action = EbayStoreCategoryAction(ebay_store=self.ebay_store)
                category_id = action.add(name=root_category)
                if not category_id:
                    return (None, None)
                result = EbayStoreCategoryModelManager.create(ebay_store=self.ebay_store, category_id=category_id, name=root_category)
                if not result:
                    return (None, None)
                return (category_id, root_category)
        except Exception as e:
            return (None, None)

    def __revise(self, ebay_item, pictures):
        action = EbayItemAction(ebay_store=self.ebay_store, ebay_item=ebay_item, amazon_item=ebay_item.amazon_item)

        picture_urls = []
        if pictures and pictures.count() > 0:
            picture_urls = action.upload_pictures(pictures)
            if len(picture_urls) < 1:
                if action.end_item():
                    EbayItemModelManager.inactive(ebay_item=ebay_item)
                logger.error("[%s|ASIN:%s] No item pictures available - inactive/end item" % (self.ebay_store.username, ebay_item.amazon_item.asin))
                return (False, False)
        store_category_id, store_category_name = self.__find_ebay_store_category_info(amazon_category=ebay_item.amazon_item.category)
        return action.revise_item(picture_urls=picture_urls, store_category_id=store_category_id)

    def __build_variations_common_title(self, amazon_items):
        # TODO: need to improve
        try:
            return amazon_items.first().title
        except Exception as e:
            return None

    def __build_variations_common_description(self, amazon_items):
        # TODO: need to improve
        try:
            return amazon_items.first().description
        except Exception as e:
            return None

    def __get_variations_common_pictures(self, amazon_items):
        if amazon_items.count() < 1:
            return []
        else:
            common_picture_set = None
            for a in amazon_items:
                if common_picture_set is None:
                    common_picture_set = set([ p.picture_url for p in AmazonItemPictureModelManager.fetch(asin=a.asin) ])
                else:
                    common_picture_set = common_picture_set & set([ p.picture_url for p in AmazonItemPictureModelManager.fetch(asin=a.asin) ])
            return list(common_picture_set)

    def __build_variations_variation_specifics_set(self, amazon_items):
        # build simpler dict first
        name_value_sets = {}
        for a in amazon_items:
            specifics = json.loads(a.variation_specifics)
            for key, val in specifics.iteritems():
                if key in name_value_sets:
                    name_value_sets[key].append(val)
                    name_value_sets[key] = list(set(name_value_sets[key])) # remove dups
                else:
                    name_value_sets[key] = [val, ]
        # convert dict to ebay variation specifics set format
        name_value_list = []
        for name, vals in name_value_sets.iteritems():
            name_value_list.append({
                "Name": name,
                "Value": vals,
            })
        return { "NameValueList": name_value_list }

    def __build_variations_variation(self, amazon_items):
        variations = []
        for amazon_item in amazon_items:
            start_price = amazonmws_utils.calculate_profitable_price(amazon_item.price, self.ebay_store)
            quantity = 0
            if amazon_item.is_listable(ebay_store=self.ebay_store, excl_brands=self.__excl_brands):
                quantity = amazonmws_settings.EBAY_ITEM_DEFAULT_QUANTITY
            try:
                specs = json.loads(amazon_item.specifications)
            except TypeError as e:
                specs = []
            except ValueError as e:
                specs = []
            mpn = amazonmws_utils.get_mpn(specs=specs)
            upc = amazonmws_utils.get_upc(specs=specs)
            variations.append({
                "SKU": amazon_item.asin,
                "StartPrice": start_price,
                "Quantity": quantity,
                "VariationProductListingDetails": amazonmws_utils.build_ebay_product_listing_details(brand=amazon_item.brand_name, mpn=mpn, upc=upc),
                "VariationSpecifics": self.__build_ebay_item_variation_specifics(amazon_item_variation_specifis=amazon_item.variation_specifics),
            })
        return variations

    def __build_ebay_item_variation_specifics(self, amazon_item_variation_specifis=None):
        if amazon_item_variation_specifis is None:
            return {}
        nv_list = []
        variations = json.loads(amazon_item_variation_specifis)
        for key, val in variations.iteritems():
            nv_list.append({ "Name": key, "Value": val })
        return { "NameValueList": nv_list }

    def __get_variations_pictures_variation_specific_name(self, amazon_items):
        _specifics = json.loads(amazon_items.first().variation_specifics)
        if len(_specifics) == 1:
            return next(_specifics.__iter__())
        else:
            # 'color' always takes VariationSpecificName
            for key in _specifics:
                if 'color' in key.lower() or 'colour' in key.lower():
                    return key
            # 0. find VariationSpecificName among all available names in specifics
            # 1. get all picture_urls along with variation_specifics
            # 2. seperate pictures per VariationSpecificValue
            #       - and remove common_pictures
            # 3. build ebay variations Pictures format
            #
            # this works only at ideal situation, but would not work in real data...
            # assume first specific is VariationSpecificName for now...
            _compaired_s = None
            _compaired_pics = []
            for a in amazon_items:
                if len(_compaired_pics) < 1:
                    _compaired_s = json.loads(a.variation_specifics)
                    _compaired_pics = [ p.picture_url for p in AmazonItemPictureModelManager.fetch(asin=a.asin) ]
                    continue
                current_s = json.loads(a.variation_specifics)
                current_pics = [ p.picture_url for p in AmazonItemPictureModelManager.fetch(asin=a.asin) ]
                if set(_compaired_pics).issubset(set(current_pics)) and set(current_pics).issubset(set(_compaired_pics)): # same pics: same value key should be VariationSpecificName
                    for _key1, _val1 in _compaired_s:
                        for _key2, _val2  in current_s:
                            if _key1 == _key2 and _val1 == _val2:
                                return _key1

                else: # different pics: different value key should be VariationSpecificName
                    for _key1, _val1 in _compaired_s:
                        for _key2, _val2 in current_s:
                            if _key1 == _key2 and _val1 != _val2:
                                return _key1
        return None

    def __build_variations_pictures(self, amazon_items, common_pictures):
        ret = {}
        v_specifics_name = self.__get_variations_pictures_variation_specific_name(amazon_items=amazon_items)
        if v_specifics_name is None:
            return {}

        vs_picture_set_list = []
        _vs_picture_set = {}
        for a in amazon_items:
            specifics = json.loads(a.variation_specifics)
            if specifics[v_specifics_name] not in _vs_picture_set:
                _vs_picture_set[specifics[v_specifics_name]] = list(set([ p.picture_url for p in AmazonItemPictureModelManager.fetch(asin=a.asin) ]) - set(common_pictures))
        for key, val in _vs_picture_set.iteritems():
            vs_picture_set_list.append({
                "VariationSpecificValue": key,
                "PictureURL": val,
            })
        return {
            "VariationSpecificName": v_specifics_name,
            "VariationSpecificPictureSet": vs_picture_set_list,
        }

    def __build_variations_obj(self, amazon_items, common_pictures):
        """i.e
            {
                "VariationSpecificsSet": 
                {
                    "NameValueList": [
                        {
                            "Name": "Size",
                            "Value": [
                                "XS",
                                "S",
                                "M",
                            ]
                        },
                        {
                            "Name": "Color",
                            "Value": [
                                "Black",
                                "Pink",
                                "Yellow",
                            ]
                        },
                    ],
                },
                "Variation": [
                    {
                        "SKU": xxxx,
                        "StartPrice": 20.99,
                        "Quantity": 1,
                        "VariationSpecifics": {
                            "NameValueList": [
                                {
                                    "Name": "Color",
                                    "Value": "Pink",
                                },
                                {
                                    "Name": "Size",
                                    "Value": "S",
                                },
                            ],
                        },
                    },
                    {
                        "SKU": xxxx,
                        "StartPrice": 25.99,
                        "Quantity": 1,
                        "VariationSpecifics": {
                            "NameValueList": [
                                {
                                    "Name": "Color",
                                    "Value": "Yellow",
                                },
                                {
                                    "Name": "Size",
                                    "Value": "M",
                                },
                            ],
                        },
                    },
                    {
                        "SKU": xxxx,
                        "StartPrice": 15.99,
                        "Quantity": 1,
                        "VariationSpecifics": {
                            "NameValueList": [
                                {
                                    "Name": "Color",
                                    "Value": "Black",
                                },
                                {
                                    "Name": "Size",
                                    "Value": "XS",
                                },
                            ],
                        },
                    },
                ],
                "Pictures": {
                    "VariationSpecificName": "Color",
                    "VariationSpecificPictureSet": [
                        {
                            "VariationSpecificValue": "Black",
                            "PictureURL": [
                                "http://i4.ebayimg.ebay.com/01/i/000/77/3c/d88f_1_sbl.JPG",
                            ],
                        },
                        {
                            "VariationSpecificValue": "Pink",
                            "PictureURL": [
                                "http://i12.ebayimg.com/03/i/04/8a/5f/a1_1_sbl.JPG",
                                "http://i12.ebayimg.com/03/i/04/8a/5f/a1_1_sb2.JPG",
                            ],
                        },
                        {
                            "VariationSpecificValue": "Yellow",
                            "PictureURL": [
                                "http://i4.ebayimg.ebay.com/01/i/000/77/3c/d89f_1_sbl.JPG",
                            ],
                        },
                    ],
                },
            }
        """
        return {
            "VariationSpecificsSet": self.__build_variations_variation_specifics_set(amazon_items=amazon_items),
            "Variation": self.__build_variations_variation(amazon_items=amazon_items),
            "Pictures": self.__build_variations_pictures(amazon_items=amazon_items, 
                common_pictures=common_pictures),
        }

    def __build_delete_variations_obj(self, deleting_asins=[]):
        """ i.e.
            {
                "Variation": [
                    {
                        "Delete": True,
                        "SKU": xxxx,
                    },
                    {
                        "Delete": True,
                        "SKU": xxxx,
                    },
                ],
            }
        """
        variations = []
        for asin in deleting_asins:
            variations.append({
                "Delete": True,
                "SKU": asin,
            })
        return {
            "Variation": variations
        }

    def __build_add_variations_obj(self, amazon_items, common_pictures, adding_asins=[]):
        """ i.e.
            {
                "VariationSpecificsSet": 
                {
                    "NameValueList": [
                        {
                            "Name": "Size",
                            "Value": [
                                "XS",
                                "S",
                                "M",
                            ]
                        },
                        {
                            "Name": "Color",
                            "Value": [
                                "Black",
                                "Pink",
                                "Yellow",
                            ]
                        },
                    ],
                },
                "Variation": [ # new variations only
                    {
                        "SKU": xxxx,
                        "StartPrice": 20.99,
                        "Quantity": 1,
                        "VariationSpecifics": {
                            "NameValueList": [
                                {
                                    "Name": "Color",
                                    "Value": "Pink",
                                },
                                {
                                    "Name": "Size",
                                    "Value": "S",
                                },
                            ],
                        },
                    },
                    {
                        "SKU": xxxx,
                        "StartPrice": 25.99,
                        "Quantity": 1,
                        "VariationSpecifics": {
                            "NameValueList": [
                                {
                                    "Name": "Color",
                                    "Value": "Yellow",
                                },
                                {
                                    "Name": "Size",
                                    "Value": "M",
                                },
                            ],
                        },
                    },
                    {
                        "SKU": xxxx,
                        "StartPrice": 15.99,
                        "Quantity": 1,
                        "VariationSpecifics": {
                            "NameValueList": [
                                {
                                    "Name": "Color",
                                    "Value": "Black",
                                },
                                {
                                    "Name": "Size",
                                    "Value": "XS",
                                },
                            ],
                        },
                    },
                ],
                "Pictures": {
                    "VariationSpecificName": "Color",
                    "VariationSpecificPictureSet": [
                        {
                            "VariationSpecificValue": "Black",
                            "PictureURL": [
                                "http://i4.ebayimg.ebay.com/01/i/000/77/3c/d88f_1_sbl.JPG",
                            ],
                        },
                        {
                            "VariationSpecificValue": "Pink",
                            "PictureURL": [
                                "http://i12.ebayimg.com/03/i/04/8a/5f/a1_1_sbl.JPG",
                                "http://i12.ebayimg.com/03/i/04/8a/5f/a1_1_sb2.JPG",
                            ],
                        },
                        {
                            "VariationSpecificValue": "Yellow",
                            "PictureURL": [
                                "http://i4.ebayimg.ebay.com/01/i/000/77/3c/d89f_1_sbl.JPG",
                            ],
                        },
                    ],
                },
            }
        """
        return {
            "VariationSpecificsSet": self.__build_variations_variation_specifics_set(amazon_items=amazon_items),
            "Variation": self.__build_variations_variation(amazon_items=AmazonItemModelManager.fetch(asin__in=adding_asins)),
            "Pictures": self.__build_variations_pictures(amazon_items=amazon_items, 
                common_pictures=common_pictures),
        }

    def __build_modify_variations_obj(self, modifying_asins=[]):
        """i.e
            {
                "Variation": [ # modifying variations only
                    {
                        "SKU": xxxx,
                        "StartPrice": 20.99,
                        "Quantity": 1,
                        "VariationSpecifics": {
                            "NameValueList": [
                                {
                                    "Name": "Color",
                                    "Value": "Pink",
                                },
                                {
                                    "Name": "Size",
                                    "Value": "S",
                                },
                            ],
                        },
                    },
                    {
                        "SKU": xxxx,
                        "StartPrice": 25.99,
                        "Quantity": 1,
                        "VariationSpecifics": {
                            "NameValueList": [
                                {
                                    "Name": "Color",
                                    "Value": "Yellow",
                                },
                                {
                                    "Name": "Size",
                                    "Value": "M",
                                },
                            ],
                        },
                    },
                    {
                        "SKU": xxxx,
                        "StartPrice": 15.99,
                        "Quantity": 1,
                        "VariationSpecifics": {
                            "NameValueList": [
                                {
                                    "Name": "Color",
                                    "Value": "Black",
                                },
                                {
                                    "Name": "Size",
                                    "Value": "XS",
                                },
                            ],
                        },
                    },
                ],
            }
        """
        return {
            "Variation": self.__build_variations_variation(amazon_items=AmazonItemModelManager.fetch(asin__in=modifying_asins)),
        }

    def __compare_item_variations(self, amazon_items, ebay_item):
        """ delete: any variations which name and specifics deleted
            add: any variations which name and specifics newly added
            modify: all variations only price/quantity updated/changed

            return value: i.e.
            {
                'delete': ['B00E98O7GC', ...],
                'add': ['B00E98O7GC', 'B00E98O7GC', ...],
                'modify': ['B00E98O7GC', 'B00E98O7GC', 'B00E98O7GC', ...],
            }
        """
        ret = {
            'delete': [],
            'add': [],
            'modify': [],
        }

        ebay_item_variations = EbayItemModelManager.fetch_variations(ebay_item=ebay_item)
        if not ebay_item_variations:
            ret['add'] = [ a.asin for a in amazon_items ]
            return ret

        amazon_v_asin_set = set([ a.asin for a in amazon_items ])
        ebay_v_asin_set = set([ e.asin for e in ebay_item_variations ])

        ret['delete'] = list(ebay_v_asin_set - amazon_v_asin_set)
        ret['add'] = list(amazon_v_asin_set - ebay_v_asin_set)

        _modifying_list = list(ebay_v_asin_set - (ebay_v_asin_set - amazon_v_asin_set))
        for _m_asin in _modifying_list:
            for a in amazon_items:
                if a.asin != _m_asin:
                    continue
                for e in ebay_item_variations:
                    if e.asin != _m_asin:
                        continue
                    if a.variation_specifics != e.specifics:
                        if _m_asin not in ret['delete']:
                            ret['delete'].append(_m_asin)
                        if _m_asin not in ret['add']:
                            ret['add'].append(_m_asin)
                    else:
                        ret['modify'].append(_m_asin)
        return ret

    def __revise_v(self, amazon_items, ebay_item):
        # multi-variation item only
        if not ebay_item:
            return (False, False)
        else:
            action = EbayItemAction(ebay_store=self.ebay_store, ebay_item=ebay_item, amazon_item=amazon_items.first())
            # get common title/pictures, variation object
            common_pictures = self.__get_variations_common_pictures(amazon_items=amazon_items)
            store_category_id, store_category_name = self.__find_ebay_store_category_info(amazon_category=amazon_items.first().category)

            # compare amazon_items variations with existing(ebay_items) variations
            # 1. if there are new variation from amazon_items variations
            #   apply action.add_variations(ebay_item, variations)
            # 2. if there are deleting variations from ebay_items variations
            #   apply action.delete_variations(ebay_item, variations)
            # 3. modify all other variations
            #   apply action.modify_variations(ebay_item, variations)
            variation_comp_result = self.__compare_item_variations(
                amazon_items=amazon_items, ebay_item=ebay_item)

            if 'delete' in variation_comp_result and len(variation_comp_result['delete']) > 0:
                if action.update_variations(variations=self.__build_delete_variations_obj(
                        deleting_asins=variation_comp_result['delete'])):
                    # db update
                    EbayItemVariationModelManager.delete(ebid=ebay_item.ebid,
                        asin__in=variation_comp_result['delete'])

            if 'add' in variation_comp_result and len(variation_comp_result['add']) > 0:
                adding_variations_obj = self.__build_add_variations_obj(amazon_items=amazon_items, 
                        common_pictures=common_pictures, 
                        adding_asins=variation_comp_result['add'])
                if action.update_variations(variations=adding_variations_obj):
                    # db update
                    for v in adding_variations_obj['Variation']:
                        a = AmazonItemModelManager.fetch_one(asin=v['SKU'])
                        if a is None:
                            continue
                        variation_db_obj = EbayItemVariationModelManager.fetch_one(ebid=ebay_item.ebid,
                            asin=v['SKU'])
                        if not variation_db_obj:
                            EbayItemVariationModelManager.create(ebay_item=ebay_item,
                                                        ebid=ebay_item.ebid,
                                                        asin=v['SKU'],
                                                        specifics=a.variation_specifics,
                                                        eb_price=v['StartPrice'],
                                                        quantity=v['Quantity'])
                        else:
                            EbayItemVariationModelManager.update(variation=variation_db_obj,
                                                        specifics=a.variation_specifics,
                                                        eb_price=v['StartPrice'],
                                                        quantity=v['Quantity'])

            modifying_variations_obj = {}
            if 'modify' in variation_comp_result and len(variation_comp_result['modify']) > 0:
                # price/inventory update
                for m_asin in variation_comp_result['modify']:
                    for _a in amazon_items:
                        if _a.asin == m_asin:
                            eb_price = amazonmws_utils.calculate_profitable_price(_a.price, self.ebay_store)
                            quantity = 0
                            if _a.is_listable(ebay_store=self.ebay_store, excl_brands=self.__excl_brands):
                                quantity = amazonmws_settings.EBAY_ITEM_DEFAULT_QUANTITY
                            if action.revise_inventory(eb_price=eb_price, quantity=quantity, asin=_a.asin):
                                # db update
                                var_obj = EbayItemVariationModelManager.fetch_one(ebid=ebay_item.ebid, 
                                    asin=_a.asin)
                                EbayItemVariationModelManager.update(variation=var_obj,
                                                            eb_price=eb_price,
                                                            quantity=quantity)
                            break

            # finally revise item content (title/description/pictures/store category id) itself only
            success = action.revise_item(title=self.__build_variations_common_title(amazon_items=amazon_items),
                description=self.__build_variations_common_description(amazon_items=amazon_items),
                picture_urls=common_pictures,
                store_category_id=store_category_id)
            return (success, False)

    def __revise_title(self, ebay_item):
        action = EbayItemAction(ebay_store=self.ebay_store, ebay_item=ebay_item, amazon_item=ebay_item.amazon_item)
        return action.revise_item_title()

    def __oos(self, amazon_item, ebay_item):
        try:
            ebay_action = EbayItemAction(ebay_store=self.ebay_store, ebay_item=ebay_item, amazon_item=amazon_item)
            succeed = ebay_action.revise_inventory(eb_price=None, quantity=0, do_revise_item=False)
            if succeed:
                EbayItemModelManager.oos(ebay_item)
            return (succeed, False)
        except Exception:
            return (False, False)

    def run(self, order='rating', restockonly=False):
        """order: rating | discount, restockonly: boolean
        """
        if order == 'discount':
            items = AmazonItemModelManager.fetch_discount_for_listing(ebay_store=self.ebay_store)
            try:
                for amazon_item, ebay_item in items:
                    # in case having duplicated asin
                    if amazon_item.asin in self.__asins_exclude:
                        continue
                    succeed, maxed_out = self.run_each(amazon_item, ebay_item, restockonly)
                    if succeed:
                        self.__asins_exclude.append(amazon_item.asin)
                    if maxed_out:
                        raise GetOutOfLoop("[%s] STOP LISTING - REACHED EBAY ITEM LIST LIMITATION" % self.ebay_store.username)
            except GetOutOfLoop as e:
                logger.info(e)

        else: # rating
            pref_cats = EbayStorePreferredCategoryModelManager.fetch(ebay_store=self.ebay_store, status=1)
            try:
                for pref_cat in pref_cats:
                    items = AmazonItemModelManager.fetch_filtered_for_listing(pref_cat, 
                                self.__min_review_count, 
                                order=order,
                                asins_exclude=self.__asins_exclude,
                                listing_min_dollar=self.ebay_store.listing_min_dollar,
                                listing_max_dollar=self.ebay_store.listing_max_dollar)
                    for amazon_item, ebay_item in items:
                        count = 1
                        if count > pref_cat.max_items:
                            break
                        # in case having duplicated asin
                        if amazon_item.asin in self.__asins_exclude:
                            continue
                        succeed, maxed_out = self.run_each(amazon_item, ebay_item, restockonly)
                        if succeed:
                            self.__asins_exclude.append(amazon_item.asin)
                            count += 1
                        if maxed_out:
                            raise GetOutOfLoop("[%s] STOP LISTING - REACHED EBAY ITEM LIST LIMITATION" % self.ebay_store.username)
            except GetOutOfLoop as e:
                logger.info(e)
        return True

    def run_sold(self, order='most', restockonly=False, max_items=None):
        """order: most | recent, restockonly: boolean
        """
        try:
            count = 1
            items = AmazonItemModelManager.fetch_sold_for_listing(self.ebay_store, order)
            for amazon_item, ebay_item in items:
                if max_items and count > max_items:
                    raise GetOutOfLoop("[%s] STOP LISTING - REACHED SOLD ITEM LIST LIMITATION" % self.ebay_store.username)
                # in case having duplicated asin
                if amazon_item.asin in self.__asins_exclude:
                    continue
                succeed, maxed_out = self.run_each(amazon_item, ebay_item, restockonly)
                if succeed:
                    self.__asins_exclude.append(amazon_item.asin)
                    count += 1
                if maxed_out:
                    raise GetOutOfLoop("[%s] STOP LISTING - REACHED EBAY ITEM LIST LIMITATION" % self.ebay_store.username)
        except GetOutOfLoop as e:
            logger.info(e)
        return True

    def __is_variationable_category(self, amazon_item):
        if amazon_item.category in self.__atemap:
            category_id = self.__atemap[amazon_item.category]
        else:
            category_id = self.__find_ebay_category_id(amazon_item.title)

        return EbayCategoryFeaturesModelManager.variations_enabled(ebay_category_id=category_id)

    def run_each(self, amazon_items, ebay_item=None, restockonly=False):
        if ebay_item and EbayItemModelManager.is_inactive(ebay_item): # inactive (ended) item. do nothing
            return (False, False)

        if not amazon_items:
            return (False, False)
        if amazon_items.__class__.__name__ == 'AmazonItem': # quirk: make compatible with old code
            amazon_items = AmazonItemModelManager.fetch(parent_asin=amazon_items.parent_asin)
        # depends on number of amazon items given...
        if amazon_items.count() < 1:
            return (False, False)
        elif amazon_items.count() == 1:
            # no variation item
            amazon_item = amazon_items.first()
            if not amazon_item.is_listable(ebay_store=self.ebay_store, excl_brands=self.__excl_brands):
                if not ebay_item:
                    return (False, False)
                else:
                    return self.__oos(amazon_item=amazon_item, ebay_item=ebay_item)
            else:
                if ebay_item:
                    return self.__revise(ebay_item=ebay_item,
                        pictures=AmazonItemPictureModelManager.fetch(asin=amazon_item.asin))
                else:
                    if restockonly:
                        logger.error("[%s|ASIN:%s] no new ebay listing allowed (restock only) - no listing" % (self.ebay_store.username, amazon_item.asin))
                        return (False, False)
                    else:
                        return self.__list_new(amazon_item=amazon_item)
        else: # amazon_items.count() > 1
            # multi-variation item
            if not self.__is_variationable_category(amazon_item=amazon_items.first()):
                for a_item in amazon_items:
                    success, maxed_out = self.run_each(amazon_items=a_item, ebay_item=ebay_item, restockonly=restockonly)
                    if maxed_out:
                        return (success, maxed_out)
                return (True, False)
            else:
                if ebay_item:
                    return self.__revise_v(amazon_items=amazon_items, ebay_item=ebay_item)
                else:
                    if restockonly:
                        logger.warning("[%s|ASIN:%s] no new ebay listing allowed (restock only) - no listing" % (self.ebay_store.username, amazon_items.first().asin))
                        return (False, False)
                    else:
                        return self.__list_new_v(amazon_items=amazon_items)
        return (False, False)

    # def run_revise_pictures(self):
    #     """ deprecated
    #     """
    #     ebay_items = EbayItemModelManager.fetch(ebay_store_id=self.ebay_store.id)
    #     for ebay_item in ebay_items:
    #         one_day_before = timezone.now() - datetime.timedelta(1) # updated within last 24 hours
    #         revised_pictures = AmazonItemPictureModelManager.fetch(asin=ebay_item.asin, created_at__gte=one_day_before)
    #         if revised_pictures.count() < 1:
    #             continue
    #         self.__revise(ebay_item, pictures=revised_pictures)
    #     return True

    def revise_item(self, ebay_item):
        if not ebay_item:
            return (False, False)
        amazon_items = AmazonItemModelManager.fetch(parent_asin=ebay_item.asin)
        if amazon_items.count() < 1:
            return (False, False)
        elif amazon_items.count() == 1:
            # no variation item
            amazon_item = amazon_items.first()
            if not amazon_item.is_listable(ebay_store=self.ebay_store, excl_brands=self.__excl_brands):
                return self.__oos(amazon_item=amazon_item, ebay_item=ebay_item)
            else:
                return self.__revise(ebay_item=ebay_item,
                    pictures=AmazonItemPictureModelManager.fetch(asin=amazon_item.asin))
        else: # amazon_items.count() > 1
            # multi-variation item
            if not self.__is_variationable_category(amazon_item=amazon_items.first()):
                for a_item in amazon_items:
                    self.revise_item(ebay_item=ebay_item)
                return (True, False)
            else:
                return self.__revise_v(amazon_items=amazon_items, ebay_item=ebay_item)
        return (False, False)

    def revise_item_title(self, ebay_item):
        self.__revise_title(ebay_item=ebay_item)


class CategoryHandler(object):

    def __init__(self, ebay_store, **kwargs):
        self.ebay_store = ebay_store
        logger.addFilter(StaticFieldFilter(get_logger_name(), 'atoe_category'))

    def find_ebay_category(self, string):
        keywords = amazonmws_utils.to_keywords(string)
        if not keywords:
            return (None, None)

        ebay_action = EbayItemAction(ebay_store=self.ebay_store)
        ebay_category_info = ebay_action.find_category(keywords)
        if not ebay_category_info:
            return (None, None)
        return ebay_category_info

    def find_ebay_category_features(self, category_id):
        ebay_action = EbayItemAction(ebay_store=self.ebay_store)
        try:
            return ebay_action.get_category_features(category_id=category_id)
        except Exception as e:
            logger.exception("Failed to find ebay category features - {}".format(str(e)))
            return None

    def store_full_categories(self):
        category_action = EbayItemCategoryAction(ebay_store=self.ebay_store)
        top_level_categories = category_action.get_top_level_categories()

        if len(top_level_categories) > 0:
            self._store_categories(categories=top_level_categories)

            for category in top_level_categories:
                sub_level_categories = category_action.get_categories(parent_category_id=category.get('CategoryID'), level_limit=1000)
                self._store_categories(categories=sub_level_categories)

    def _store_categories(self, categories):
        if len(categories) < 1:
            return False

        else:
            for category in categories:
                obj = EbayItemCategoryManager.save(
                    category_id=category.get('CategoryID'),
                    category_level=int(category.get('CategoryLevel')),
                    category_name=category.get('CategoryName'),
                    category_parent_id=category.get('CategoryParentID'),
                    auto_pay_enabled=True if category.get('AutoPayEnabled', 'false') == 'true' else False,
                    best_offer_enabled=True if category.get('BestOfferEnabled', 'false') == 'true' else False,
                    leaf_category=True if category.get('LeafCategory', 'false') == 'true' else False
                )

                # print obj
            return True


class OrderShippingTrackingHandler(object):

    ebay_store = None
    amazon_account = None

    def __init__(self, ebay_store, amazon_account=None):
        self.ebay_store = ebay_store
        self.amazon_account = amazon_account
        logger.addFilter(StaticFieldFilter(get_logger_name(), 'order_shipping_tracking'))

    def set_shipping_tracking_information(self, ebay_order_id, carrier, tracking_number):
        ebay_order = EbayOrderModelManager.fetch_one(order_id=ebay_order_id)
        if not ebay_order:
            return False

        action = EbayOrderAction(ebay_store=self.ebay_store)
        result = action.set_shipping_tracking_info(ebay_order=ebay_order, 
            carrier=carrier, tracking_number=tracking_number)

        if not result:
            logger.info('[{}] failed to send tracking information to ebay - [ {} : {} ]'.format(ebay_order_id, carrier, tracking_number))
            return False
        else:
            # create new ebay_order_shippings entry
            ebay_order_shipping = EbayOrderShippingModelManager.create(order_id=ebay_order_id,
                carrier=carrier, tracking_number=tracking_number)
            if not ebay_order_shipping:
                return False

            # append tracking info into associated amazon_order entry, if possible
            ordered_pair = EbayOrderAmazonOrderModelManager.fetch_one(ebay_order_id=ebay_order_id)
            if ordered_pair and ordered_pair.amazon_order:
                AmazonOrderModelManager.update(amazon_order=ordered_pair.amazon_order,
                    carrier=carrier, tracking_number=tracking_number)

            return ebay_order_shipping


class FeedbackLeavingHandler(object):

    ebay_store = None
    amazon_account = None

    def __init__(self, ebay_store, amazon_account=None):
        self.ebay_store = ebay_store
        self.amazon_account = amazon_account
        logger.addFilter(StaticFieldFilter(get_logger_name(), 'feedback_leaving'))

    def leave_feedback(self, ebay_order):
        action = EbayOrderAction(ebay_store=self.ebay_store)
        result = action.leave_feedback(ebay_order=ebay_order)

        if not result:
            logger.info('[{}] failed leave a feedback'.format(ebay_order.order_id))
            return False
        else:
            # update ebay_order entry
            updating = EbayOrderModelManager.update(order=ebay_order, feedback_left=True)
            if not updating:
                return False
            ebay_item = EbayOrderItemModelManager.fetch(order_id=ebay_order.order_id)[:1].get()
            # send thank you message to buyer
            action.send_message_to_buyer(ebay_order=ebay_order,
                ebid=ebay_item.ebid,
                question_type="Shipping",
                subject=self.ebay_store.message_on_shipping_subject,
                body=self.ebay_store.message_on_shipping_body
            )
            return True

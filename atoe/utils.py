# -*- coding: utf-8 -*-
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'scrapers', 'amzn'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'rfi'))

import datetime
import json

from pattern.en import singularize
from django.utils import timezone

from amazonmws import settings as amazonmws_settings, utils as amazonmws_utils
from amazonmws.loggers import GrayLogger as logger, StaticFieldFilter, get_logger_name
from amazonmws.model_managers import *


class EbayItemVariationUtils(object):
    
    @staticmethod
    def build_item_specifics_for_multi_variations(ebay_category_id, amazon_item):
        """ amazon_item: django model

            Style - Shoe/Clothing specific name-value set
                To avoid ebay api error: 21919303
                Error Code 21919303 - The item specific Style is missing. The item specific Style is missing. Add Style to this listing, enter a valid value, and then try again.
        """
        try:
            name_value_list = []
            name_value_list.append({
                "Name": "Brand",
                "Value": amazonmws_utils.xml_escape(amazon_item.brand_name),
            })
            cat_map = AtoECategoryMapModelManager.fetch_one(ebay_category_id=ebay_category_id)
            if cat_map and any(sp_cat in cat_map.ebay_category_name.lower() for sp_cat in ["women's shoes", "men's shoes", "women's clothing", "men's clothing"]):
                name_value_list.append({
                    "Name": "Style",
                    "Value": amazonmws_utils.xml_escape(
                        string=EbayItemVariationUtils.convert_amazon_category_name_to_list(
                            amazon_category=amazon_item.category)[-1]),
                })
                # append Band Size/Cup Size for bras if necessary, i.e. One Size
                if all(bras in cat_map.ebay_category_name.lower() for bras in ["women's clothing", "intimates", "sleep", "bras"]):
                    name_value_list.append({"Name": "Band Size", "Value": "One Size"})
                    name_value_list.append({"Name": "Cup Size", "Value": "One Size"})
            elif cat_map and all(sp_cat in cat_map.ebay_category_name.lower() for sp_cat in ["handbags", "purses"]):
                name_value_list.append({
                    "Name": "Style",
                    "Value": amazonmws_utils.xml_escape(
                        string=singularize(EbayItemVariationUtils.convert_amazon_category_name_to_list(
                                amazon_category=amazon_item.category)[-1])),
                })
            elif cat_map and all(sp_cat in cat_map.ebay_category_name.lower() for sp_cat in ["cell", "phone", "accessories", "cases"]):
                name_value_list.append({"Name": "MPN", "Value": "Not Applicable"})
                name_value_list.append({"Name": "EAN", "Value": "Not Applicable"})
            return { "NameValueList": name_value_list }
        except Exception as e:
            logger.exception(str(e))
            return None

    @staticmethod
    def build_item_description(amazon_item):
        """ amazon_item: django model
        """
        # apparel: include size chart into description
        description = amazon_item.description
        if amazon_item.has_sizechart:
            size_chart = AmazonItemApparelModelManager.get_size_chart(parent_asin=amazon_item.parent_asin)
            if size_chart:
                description = u"{}<div id=\"reference-size-chart\" class=\"panel panel-default\"><div class=\"panel-heading\">Reference Size Chart</div><div class=\"panel-body\">{}</div></div>".format(amazon_item.description if amazon_item.description else u"", size_chart)
        return description

    @staticmethod
    def find_single_item_variation(amazon_items):
        for a in amazon_items:
            try:
                specifics = json.loads(a.variation_specifics)
            except TypeError as e:
                specifics = {}
            except ValueError as e:
                specifics = {}
            for key, val in specifics.iteritems():
                if (key.lower() == 'size' or key.lower() == 'number of items') and int(val) == 1:
                    return a
        return None

    @staticmethod
    def get_common_variation(amazon_items):
        try:
            if amazon_items.count() < 1:
                return None
        except Exception as e:
            return None
        try:
            single_item_variation = EbayItemVariationUtils.find_single_item_variation(amazon_items)
            if single_item_variation:
                return single_item_variation
            else:
                return amazon_items.first()
        except Exception as e:
            return amazon_items.first()


    @staticmethod
    def build_variations_common_title(amazon_items):
        """ amazon_item: django model
        """
        # TODO: need to improve
        try:
            common_variation = EbayItemVariationUtils.get_common_variation(amazon_items)
            if common_variation:
                return common_variation.title
            else:
                return None
        except Exception as e:
            return None

    @staticmethod
    def build_variations_common_description(amazon_items):
        """ amazon_item: django model
        """
        # TODO: need to improve
        try:
            common_variation = EbayItemVariationUtils.get_common_variation(amazon_items)
            if common_variation:
                return EbayItemVariationUtils.build_item_description(amazon_item=common_variation)
            else:
                return None
        except Exception as e:
            return None

    @staticmethod
    def get_variations_common_pictures(amazon_items):
        """ amazon_item: django model

            get first image of variations
        """
        if amazon_items.count() < 1:
            return []
        else:
            # collect all picture urls from variations
            all_pic_urls = []
            for a in amazon_items:
                all_pic_urls.append([ p.picture_url for p in AmazonItemPictureModelManager.fetch(asin=a.asin) ])

            # find the first (and valid) picture from the collection
            current = 0
            for pic_urls in all_pic_urls:
                if len(pic_urls) > current and amazonmws_utils.validate_image_size(pic_urls[current]):
                    return [pic_urls[current], ]
                current += 1
            return []

    @staticmethod
    def build_variation_specifics_name_value_list(ebay_category_id, iters):
        cat_map = AtoECategoryMapModelManager.fetch_one(ebay_category_id=ebay_category_id)
        if cat_map and any(sp_cat in cat_map.ebay_category_name.lower() for sp_cat in ["women's clothing", "men's clothing", ]):
            # append Size if necessary, i.e. One Size
            if not any("size" in _k.lower() for _k, _v in iters.iteritems()):
                iters["Size"] = "One Size"
            # append Size Type if necessary, i.e. Regular
            if "Size Type" not in iters:
                iters["Size Type"] = "Regular"
        name_value_list = []
        for name, vals in iters.iteritems():
            name_value_list.append({
                "Name": amazonmws_utils.xml_escape(EbayItemVariationUtils.convert_variation_name_if_necessary(
                            ebay_category_id=ebay_category_id,
                            variation_name=name)),
                "Value": amazonmws_utils.xml_escape(vals) if isinstance(vals, basestring) else vals,
            })
        return name_value_list


    @staticmethod
    def build_variations_variation_specifics_set(ebay_category_id, amazon_items):
        """ amazon_item: django model

            build simpler dict first
        """
        name_value_sets = {}
        for a in amazon_items:
            try:
                specifics = json.loads(a.variation_specifics)
            except TypeError as e:
                specifics = {}
            except ValueError as e:
                specifics = {}
            for key, val in specifics.iteritems():
                if key in name_value_sets:
                    try:
                        if val.upper() not in (_v.upper() for _v in name_value_sets[key]):
                            # IMPORTANT! for avoiding ebay api error code 21916582 - case insensitive check
                            name_value_sets[key].append(val)
                    except Exception as e:
                        logger.exception(str(e))
                        continue
                else:
                    name_value_sets[key] = [val, ]
        # convert dict to ebay variation specifics set format
        return {
            "NameValueList": EbayItemVariationUtils.build_variation_specifics_name_value_list(
                    ebay_category_id=ebay_category_id,
                    iters=name_value_sets)
        }

    @staticmethod
    def build_ebay_item_variation_specifics(ebay_category_id, amazon_item_variation_specifis=None):
        if amazon_item_variation_specifis is None:
            return {}
        try:
            variations = json.loads(amazon_item_variation_specifis)
        except TypeError as e:
            variations = {}
        except ValueError as e:
            variations = {}
        return {
            "NameValueList": EbayItemVariationUtils.build_variation_specifics_name_value_list(
                    ebay_category_id=ebay_category_id,
                    iters=variations)
        }

    @staticmethod
    def build_variations_variation(ebay_store, ebay_category_id, amazon_items, excl_brands):
        variations = []
        for amazon_item in amazon_items:
            if amazon_item.price < 1:
                # skip any $0.00 variations/items
                continue
            start_price = amazonmws_utils.calculate_profitable_price(amazon_item.price, ebay_store)
            quantity = 0
            if amazon_item.is_listable(ebay_store=ebay_store, excl_brands=excl_brands):
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
                "VariationSpecifics": EbayItemVariationUtils.build_ebay_item_variation_specifics(
                    ebay_category_id=ebay_category_id,
                    amazon_item_variation_specifis=amazon_item.variation_specifics),
            })
        return variations

    @staticmethod
    def get_variations_pictures_variation_specific_name(amazon_items):
        """ amazon_items: django queryset of AmazonItem(s)
        """
        if amazon_items.count() < 1:
            return None
        try:
            _specifics = json.loads(amazon_items.first().variation_specifics)
        except TypeError as e:
            _specifics = {}
        except ValueError as e:
            _specifics = {}
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
                    try:
                        _compaired_s = json.loads(a.variation_specifics)
                    except TypeError as e:
                        _compaired_s = {}
                    except ValueError as e:
                        _compaired_s = {}
                    _compaired_pics = [ p.picture_url for p in AmazonItemPictureModelManager.fetch(asin=a.asin) ]
                    continue
                try:
                    current_s = json.loads(a.variation_specifics)
                except TypeError as e:
                    current_s = {}
                except ValueError as e:
                    current_s = {}
                current_pics = [ p.picture_url for p in AmazonItemPictureModelManager.fetch(asin=a.asin) ]
                if set(_compaired_pics).issubset(set(current_pics)) and set(current_pics).issubset(set(_compaired_pics)): # same pics: same value key should be VariationSpecificName
                    for _key1, _val1 in _compaired_s.iteritems():
                        for _key2, _val2  in current_s.iteritems():
                            if _key1 == _key2 and _val1 == _val2:
                                return _key1

                else: # different pics: different value key should be VariationSpecificName
                    for _key1, _val1 in _compaired_s.iteritems():
                        for _key2, _val2 in current_s.iteritems():
                            if _key1 == _key2 and _val1 != _val2:
                                return _key1
        return None

    @staticmethod
    def build_variations_pictures(ebay_store, ebay_category_id, amazon_items, common_pictures=[]):
        """ ebay_store - django model
            amazon_items - django queryset of AmazonItem(s)
            common_pictures - list of urls(string)
        """

        ret = {}
        v_specifics_name = EbayItemVariationUtils.get_variations_pictures_variation_specific_name(amazon_items=amazon_items)
        if v_specifics_name is None:
            return {}

        vs_picture_set_list = []
        _vs_picture_set = {}

        for a in amazon_items:
            try:
                specifics = json.loads(a.variation_specifics)
            except TypeError as e:
                specifics = {}
            except ValueError as e:
                specifics = {}
            try:
                if v_specifics_name in specifics and specifics[v_specifics_name].upper() not in (_vs.upper() for _vs in _vs_picture_set):
                    # IMPORTANT! for avoiding ebay api error code 21916582 - case insensitive check
                    # upload pictures to ebay server
                    picture_urls = [ _p_url for _p_url in EbayPictureModelManager.get_ebay_picture_urls(
                        picture_urls=[ _p.picture_url for _p in AmazonItemPictureModelManager.fetch(asin=a.asin) ]) if _p_url not in common_pictures ]
                    if len(picture_urls) < 1:
                        logger.warning("[{}] No variation pictures available".format(specifics[v_specifics_name]))
                        continue
                    vs_picture_set_list.append({
                        "VariationSpecificValue": amazonmws_utils.xml_escape(specifics[v_specifics_name]),
                        "PictureURL": picture_urls[:12], # max 12 pictures allowed to each variation
                    })
                    _vs_picture_set[specifics[v_specifics_name]] = True
            except Exception as e:
                logger.exception(str(e))
                continue

        v_specifics_name = EbayItemVariationUtils.convert_variation_name_if_necessary(
            ebay_category_id=ebay_category_id,
            variation_name=v_specifics_name)
        return {
            "VariationSpecificName": amazonmws_utils.xml_escape(v_specifics_name),
            "VariationSpecificPictureSet": vs_picture_set_list,
        }

    @staticmethod
    def build_variations_obj(ebay_store, ebay_category_id, amazon_items, excl_brands, common_pictures=[]):
        """ ebay_store - django model
            amazon_items - django queryset of AmazonItem(s)            

            i.e
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
        # filter out 'Frustration-Free Packaging'
        amazon_items = amazon_items.exclude(variation_specifics__contains='Frustration-Free Packaging')
        return {
            "VariationSpecificsSet": EbayItemVariationUtils.build_variations_variation_specifics_set(
                ebay_category_id=ebay_category_id,
                amazon_items=amazon_items),
            "Variation": EbayItemVariationUtils.build_variations_variation(
                ebay_store=ebay_store,
                ebay_category_id=ebay_category_id,
                amazon_items=amazon_items,
                excl_brands=excl_brands),
            "Pictures": EbayItemVariationUtils.build_variations_pictures(ebay_store=ebay_store,
                ebay_category_id=ebay_category_id,
                amazon_items=amazon_items,
                common_pictures=common_pictures),
        }

    @staticmethod
    def build_add_variations_obj(ebay_store, ebay_category_id, amazon_items, excl_brands, common_pictures=[], adding_asins=[]):
        """ ebay_store - django model
            amazon_items - django queryset of AmazonItem(s)

            i.e.
            {
                "VariationSpecificsSet": # all possible variations (new & existing)
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
                "Pictures": { # all possible variations (new & existing)
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
        # filter out 'Frustration-Free Packaging'
        amazon_items = amazon_items.exclude(variation_specifics__contains='Frustration-Free Packaging')
        return {
            "VariationSpecificsSet": EbayItemVariationUtils.build_variations_variation_specifics_set(
                ebay_category_id=ebay_category_id,
                amazon_items=amazon_items),
            "Variation": EbayItemVariationUtils.build_variations_variation(
                ebay_store=ebay_store,
                ebay_category_id=ebay_category_id,
                amazon_items=AmazonItemModelManager.fetch(asin__in=adding_asins),
                excl_brands=excl_brands),
            "Pictures": EbayItemVariationUtils.build_variations_pictures(ebay_store=ebay_store,
                ebay_category_id=ebay_category_id,
                amazon_items=amazon_items,
                common_pictures=common_pictures),
        }

    # not being used due to following ebay api
    #   Error: Variation cannot be deleted during restricted revise. (#21916608)
    #
    # @staticmethod
    # def build_delete_variations_obj(deleting_asins=[]):
    #     """ i.e.
    #         {
    #             "Variation": [
    #                 {
    #                     "Delete": True,
    #                     "SKU": xxxx,
    #                 },
    #                 {
    #                     "Delete": True,
    #                     "SKU": xxxx,
    #                 },
    #             ],
    #         }
    #     """
    #     variations = []
    #     for asin in deleting_asins:
    #         variations.append({
    #             "Delete": True,
    #             "SKU": asin,
    #         })
    #     return {
    #         "Variation": variations
    #     }

    # not being used / error on it
    #
    # @staticmethod
    # def build_modify_variations_obj(ebay_store, excl_brands, modifying_asins=[], is_shoe=False):
    #     """i.e
    #         {
    #             "Variation": [ # modifying variations only
    #                 {
    #                     "SKU": xxxx,
    #                     "StartPrice": 20.99,
    #                     "Quantity": 1,
    #                     "VariationSpecifics": {
    #                         "NameValueList": [
    #                             {
    #                                 "Name": "Color",
    #                                 "Value": "Pink",
    #                             },
    #                             {
    #                                 "Name": "Size",
    #                                 "Value": "S",
    #                             },
    #                         ],
    #                     },
    #                 },
    #                 {
    #                     "SKU": xxxx,
    #                     "StartPrice": 25.99,
    #                     "Quantity": 1,
    #                     "VariationSpecifics": {
    #                         "NameValueList": [
    #                             {
    #                                 "Name": "Color",
    #                                 "Value": "Yellow",
    #                             },
    #                             {
    #                                 "Name": "Size",
    #                                 "Value": "M",
    #                             },
    #                         ],
    #                     },
    #                 },
    #                 {
    #                     "SKU": xxxx,
    #                     "StartPrice": 15.99,
    #                     "Quantity": 1,
    #                     "VariationSpecifics": {
    #                         "NameValueList": [
    #                             {
    #                                 "Name": "Color",
    #                                 "Value": "Black",
    #                             },
    #                             {
    #                                 "Name": "Size",
    #                                 "Value": "XS",
    #                             },
    #                         ],
    #                     },
    #                 },
    #             ],
    #         }
    #     """
    #     amazon_items = AmazonItemModelManager.fetch(asin__in=modifying_asins)
    #     return {
    #         "Variation": EbayItemVariationUtils.build_variations_variation(ebay_store=ebay_store, amazon_items=amazon_items, excl_brands=excl_brands, is_shoe=is_shoe),
    #     }

    @staticmethod
    def compare_item_variations(amazon_items, ebay_item):
        """ amazon_items - django queryset of AmazonItem(s)
            ebay_item - django model

            delete: any variations which name and specifics deleted
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

        amazon_v_asin_set = set([ a.asin for a in amazon_items ]) # correct/new reference
        ebay_v_asin_set = set([ e.asin for e in ebay_item_variations ]) # old reference

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

    @staticmethod
    def convert_variation_name_if_necessary(ebay_category_id, variation_name):
        """ to avoid ebay api error: 21919303
            Error, Code: 21919303, The item specific Size (Men's) is missing. The item specific Size (Men's) is missing. Add Size (Men's) to this listing, enter a valid value, and then try again.
            only affect with variation name Size
        """
        if variation_name.lower() == 'size':
            cat_map = AtoECategoryMapModelManager.fetch_one(ebay_category_id=ebay_category_id)
            if not cat_map:
                return variation_name
            if "women's shoes" in cat_map.ebay_category_name.lower():
                return "US Shoe Size (Women's)"
            if "men's shoes" in cat_map.ebay_category_name.lower():
                return "US Shoe Size (Men's)"
            if "women's clothing" in cat_map.ebay_category_name.lower():
                if any(bot in cat_map.ebay_category_name.lower() for bot in ["pants", "skirts", "jeans", "leggings"]):
                    return "Bottoms Size (Women's)"
                elif all(intim in cat_map.ebay_category_name.lower() for intim in ["intimates", "sleep"]):
                    if "bras" in cat_map.ebay_category_name.lower():
                        return "Size"
                    else:
                        return "Intimates & Sleep Size (Women's)"
                else:
                    return "Size (Women's)"
            if "men's clothing" in cat_map.ebay_category_name.lower():
                if any(bot in cat_map.ebay_category_name.lower() for bot in ["pants", "underwear", "jeans"]):
                    return "Bottoms Size (Men's)"
                else:
                    return "Size (Men's)"
        return variation_name

    @staticmethod
    def convert_amazon_category_name_to_list(amazon_category, delimiter=':'):
        return [ c.strip() for c in amazon_category.split(delimiter) ]


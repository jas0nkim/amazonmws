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

from atoe.actions import EbayItemAction


class EbayItemVariationUtils(object):
    
    @staticmethod
    def is_shoe(category_id):
        cat_maps = AtoECategoryMapModelManager.fetch(ebay_category_id=category_id)
        if cat_maps and cat_maps.count() > 0 and "women's shoes" in cat_maps.first().ebay_category_name.lower():
            return "women"
        elif cat_maps and cat_maps.count() > 0 and "men's shoes" in cat_maps.first().ebay_category_name.lower():
            return "men"
        else:
            return False

    @staticmethod
    def build_item_specifics_for_shoe(amazon_item):
        """ amazon_item: django model
        """
        try:
            return {
                    "NameValueList": [
                        {
                            "Name": "Brand",
                            "Value": amazon_item.brand_name,
                        },
                        {
                            "Name": "Style",
                            "Value": amazonmws_utils.xml_escape(
                                string=amazonmws_utils.convert_amazon_category_name_to_list(
                                    amazon_category=amazon_item.category)[-1]),
                        },
                    ],
                }
        except Exception as e:
            logger.exception(str(e))
            return None

    @staticmethod
    def build_item_specifics_for_multi_variations(amazon_item):
        """ amazon_item: django model
        """
        try:
            return {
                    "NameValueList": [
                        {
                            "Name": "Brand",
                            "Value": amazon_item.brand_name,
                        },
                    ],
                }
        except Exception as e:
            logger.exception(str(e))
            return None

    @staticmethod
    def build_item_description(amazon_item):
        """ amazon_item: django model
        """
        # apparel: include size chart into description
        size_chart = AmazonItemApparelModelManager.get_size_chart(parent_asin=amazon_item.parent_asin)
        if size_chart:
            description = u"{}{}".format(amazon_item.description if amazon_item.description else u"", size_chart)
        else:
            description = amazon_item.description
        return description

    @staticmethod
    def build_variations_common_title(amazon_items):
        """ amazon_item: django model
        """
        # TODO: need to improve
        try:
            return amazon_items.first().title
        except Exception as e:
            return None

    @staticmethod
    def build_variations_common_description(amazon_items):
        """ amazon_item: django model
        """
        # TODO: need to improve
        try:
            return EbayItemVariationUtils.build_item_description(amazon_item=amazon_items.first())
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
    def build_variations_variation_specifics_set(amazon_items, is_shoe=False):
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
                    name_value_sets[key].append(val)
                    name_value_sets[key] = list(set(name_value_sets[key])) # remove dups
                else:
                    name_value_sets[key] = [val, ]
        # convert dict to ebay variation specifics set format
        name_value_list = []
        for name, vals in name_value_sets.iteritems():
            if (is_shoe == 'women' or is_shoe == 'men') and name == 'Size':
                name = amazonmws_utils.convert_to_ebay_shoe_variation_name(is_shoe)
            name_value_list.append({
                "Name": name,
                "Value": vals,
            })
        return { "NameValueList": name_value_list }

    @staticmethod
    def build_ebay_item_variation_specifics(amazon_item_variation_specifis=None, is_shoe=False):
        if amazon_item_variation_specifis is None:
            return {}
        nv_list = []
        try:
            variations = json.loads(amazon_item_variation_specifis)
        except TypeError as e:
            variations = {}
        except ValueError as e:
            variations = {}
        for key, val in variations.iteritems():
            if (is_shoe == 'women' or is_shoe == 'men') and key == 'Size':
                key = amazonmws_utils.convert_to_ebay_shoe_variation_name(is_shoe)
            nv_list.append({ "Name": key, "Value": val })
        return { "NameValueList": nv_list }

    @staticmethod
    def build_variations_variation(ebay_store, amazon_items, excl_brands, is_shoe=False):
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
                "VariationSpecifics": EbayItemVariationUtils.build_ebay_item_variation_specifics(amazon_item_variation_specifis=amazon_item.variation_specifics,
                    is_shoe=is_shoe),
            })
        return variations

    @staticmethod
    def get_variations_pictures_variation_specific_name(amazon_items):
        """ amazon_items: django queryset of AmazonItem(s)
        """
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
    def build_variations_pictures(ebay_store, amazon_items, common_pictures=[], is_shoe=False):
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

        action = EbayItemAction(ebay_store=ebay_store, amazon_item=amazon_items.first())
        for a in amazon_items:
            try:
                specifics = json.loads(a.variation_specifics)
            except TypeError as e:
                specifics = {}
            except ValueError as e:
                specifics = {}
            if v_specifics_name in specifics and specifics[v_specifics_name] not in _vs_picture_set:
                # upload pictures to ebay server
                picture_urls = [ p.picture_url for p in AmazonItemPictureModelManager.fetch(asin=a.asin) if p.picture_url not in common_pictures ]
                picture_urls = action.upload_pictures(picture_urls)
                vs_picture_set_list.append({
                    "VariationSpecificValue": specifics[v_specifics_name],
                    "PictureURL": picture_urls[:12], # max 12 pictures allowed to each variation
                })
                _vs_picture_set[specifics[v_specifics_name]] = True

        if (is_shoe == 'women' or is_shoe == 'men') and v_specifics_name == 'Size':
            v_specifics_name = amazonmws_utils.convert_to_ebay_shoe_variation_name(is_shoe)
        return {
            "VariationSpecificName": v_specifics_name,
            "VariationSpecificPictureSet": vs_picture_set_list,
        }

    @staticmethod
    def build_variations_obj(ebay_store, amazon_items, excl_brands, common_pictures=[], is_shoe=False):
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
        return {
            "VariationSpecificsSet": EbayItemVariationUtils.build_variations_variation_specifics_set(amazon_items=amazon_items, is_shoe=is_shoe),
            "Variation": EbayItemVariationUtils.build_variations_variation(
                ebay_store=ebay_store,
                amazon_items=amazon_items,
                excl_brands=excl_brands,
                is_shoe=is_shoe),
            "Pictures": EbayItemVariationUtils.build_variations_pictures(ebay_store=ebay_store,
                amazon_items=amazon_items,
                common_pictures=common_pictures,
                is_shoe=is_shoe),
        }

    @staticmethod
    def build_add_variations_obj(ebay_store, amazon_items, excl_brands, common_pictures=[], adding_asins=[], is_shoe=False):
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
        return {
            "VariationSpecificsSet": EbayItemVariationUtils.build_variations_variation_specifics_set(amazon_items=amazon_items, is_shoe=is_shoe),
            "Variation": EbayItemVariationUtils.build_variations_variation(
                ebay_store=ebay_store,
                amazon_items=AmazonItemModelManager.fetch(asin__in=adding_asins),
                excl_brands=excl_brands,
                is_shoe=is_shoe),
            "Pictures": EbayItemVariationUtils.build_variations_pictures(ebay_store=ebay_store,
                amazon_items=amazon_items,
                common_pictures=common_pictures,
                is_shoe=is_shoe),
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

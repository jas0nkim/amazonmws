import urllib2
import os
import time
import json
import requests
import re

from decimal import Decimal
from uuid import UUID

from PIL import Image
from StringIO import StringIO

from jinja2 import Template

from ebaysdk.finding import Connection as Finding
from ebaysdk.exception import ConnectionError

from .loggers import GrayLogger as logger
from . import settings


class SpecialTypedJSONEncoder(json.JSONEncoder):

    def default(self, obj):
        """override parent method
        """

        # avoid TypeError: UUID is not JSON serializable
        if isinstance(obj, UUID):
            return str(obj)

        # avoid TypeError: Decimal is not JSON serializable
        elif isinstance(obj, Decimal):
            return str(obj)
        
        return json.JSONEncoder.default(self, obj)


def validate_url(url):
    ret = False

    try:
        urllib2.urlopen(url)
        ret = True

    except urllib2.HTTPError, e:
        logger.exception(e)

    except urllib2.URLError, e:
        logger.exception(e)

    return ret

def validate_image_size(url):
    response = requests.get(url)
    try:
        img = Image.open(StringIO(response.content))
    except IOError, e:
        logger.exception(e)
        return False

    (width, height) = img.size

    if width < 500 and height < 500:
        logger.error("Image width and height are less then 500px")
        return False
    return True

def dict_to_unicode(dictionary):
    return str_to_unicode(str(dictionary))

def dict_to_json_string(dictionary):
    return json.dumps(dictionary, ensure_ascii=False, cls=SpecialTypedJSONEncoder)

def str_to_unicode(string):
    if isinstance(string, unicode):
        # already unicode
        return string
    return string.decode('unicode-escape')

def money_to_float(string):
    # trim everything except number and dot(.)
    return float(re.sub(r'[^\d.]+', '', string))

def number_to_dcmlprice(number):
    return Decimal(number).quantize(Decimal('1.00'))

def to_string(val):
    if isinstance(val, str):
        # already string
        return val
    return str(val)

def extract_int(string):
    # trim everything except number
    return int(re.sub(r'[^\d]+', '', string))

def merge_two_dicts(x, y):
    return dict(x.items() + y.items())

def strip_special_characters(string, convert_to=' '):
    return re.sub(r'[^a-zA-Z\d\s:\-_,]', convert_to, string)

def is_valid_amazon_item_url(url):
    return re.match(settings.AMAZON_ITEM_LINK_PATTERN, url)

def extract_asin_from_url(url):
    match = is_valid_amazon_item_url(url)
    if match:
        return match.group(2)
    else:
        return None

def extract_seller_id_from_uri(uri):
    match = re.match(r'^.+?(?=seller=)([^&]+).*$', uri)
    if match:
        return match.group(1).replace('seller=', '').strip()
    else:
        return None


def apply_ebay_listing_template(amazon_item, ebay_store):
    if not ebay_store.item_description_template or ebay_store.item_description_template == "":
        template = settings.EBAY_STORE_DEFAULT_ITEM_DESCRIPTION_TEMPLATE
    else:
        template = ebay_store.item_description_template

    t = Template(template)
    return t.render(asin=amazon_item.asin,
        title=amazon_item.title, 
        description=amazon_item.description, 
        features=amazon_item.features, 
        policy_shipping=ebay_store.policy_shipping,
        policy_payment=ebay_store.policy_payment,
        policy_return=ebay_store.policy_return
    )

#
# DEPRECATED
# 
# def get_policy_for_ebay_item_description():
#     return  """<div class="container-fluid">
#     <br/>
#     <hr/>
#     <br/>
#     <div class="panel panel-rfi">
#         <div class="panel-heading">Shipping information</div>
#         <div class="panel-body">
#             %s
#         </div>
#     </div>
#     <div class="panel panel-rfi">
#         <div class="panel-heading">Payment information</div>
#         <div class="panel-body">
#             %s
#         </div>
#     </div>
#     <div class="panel panel-rfi">
#         <div class="panel-heading">Return policy</div>
#         <div class="panel-body">
#             %s
#         </div>
#     </div>
#     </div>""" % (settings.EBAY_STORE_DEFAULT_POLICY_SHIPPING, 
#         settings.EBAY_STORE_DEFAULT_POLICY_PAYMENT, 
#         settings.EBAY_STORE_DEFAULT_POLICY_RETURN)

def take_screenshot(webdriver, filename=None):
    if filename == None:
        filename = str(time.time()) + '.png'

    webdriver.get_screenshot_as_file(os.path.join(os.path.dirname(__file__), os.pardir, 'ss', filename))

def calculate_profitable_price(amazon_item_price, ebay_store):
    """i.e. with 3 percent margin
        
        ((cost * 1.10 * 1.09 + .20) * 1.029 + .30) * 1.03

        - * i.e. 1.07:   7 percent fixed sales tax - also charged on amazon.com
        - * 1.09:   9 percent final value fee charged by ebay
        - + .20:    20 cent listing fee charged by ebay
        - * 1.029:  2.9 percent transaction fee charged by paypal
        - + .30:    30 cent transaction fee by paypal
        - * 1.03:   and my 3 percent margin or $2.50 whichever comes less
    """
    
    profitable_price = -1

    margin_percentage = ebay_store.margin_percentage if ebay_store.margin_percentage != None else settings.APP_EBAY_LISTING_MARGIN_PERCENTAGE
    margin_max_dollar = ebay_store.margin_max_dollar if ebay_store.margin_max_dollar != None else settings.settings.APP_EBAY_LISTING_MARGIN_MAX_DOLLAR
    use_salestax_table = ebay_store.use_salestax_table
    fixed_salestax_percentage = ebay_store.fixed_salestax_percentage

    try:
        if use_salestax_table:
            cost = (float(amazon_item_price) * 1.09 + 0.20) * 1.029 + 0.30
        else:
            cost = (float(amazon_item_price) * (1.0 + float(fixed_salestax_percentage) / 100) * 1.09 + 0.20) * 1.029 + 0.30
        margin_calculated = cost * (float(margin_percentage) / 100)
        actual_margin = margin_calculated if margin_calculated < margin_max_dollar else margin_max_dollar
        
        profitable_price = number_to_dcmlprice(cost + actual_margin)

    except Exception:
        logger.exception("Unable to calculate profitable price")

    return profitable_price

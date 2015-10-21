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

def str_to_unicode(str):
    return str.decode('unicode-escape')

def merge_two_dicts(x, y):
    return dict(x.items() + y.items())

def strip_special_characters(str, convert_to=' '):
    return re.sub(r'[^a-zA-Z\d\s:\-_,]', convert_to, str)

def apply_ebay_listing_template(desc, policy_shipping=None, policy_payment=None, policy_return=None):
    if desc:
        html = """<div class="panel panel-rfi">
            <div class="panel-heading">Description</div>
            <div class="panel-body">
                %s
            </div>
        </div>""" % desc

    if policy_shipping:
        html += """<div class="panel panel-rfi">
            <div class="panel-heading">Shipping information</div>
            <div class="panel-body">
                %s
            </div>
        </div>""" % policy_shipping
    
    if policy_payment:
        html += """<div class="panel panel-rfi">
            <div class="panel-heading">Payment information</div>
            <div class="panel-body">
                %s
            </div>
        </div>""" % policy_payment
    
    if policy_return:
        html += """<div class="panel panel-rfi">
            <div class="panel-heading">Return policy</div>
            <div class="panel-body">
                %s
            </div>
        </div>""" % policy_return

    return settings.EBAY_ITEM_DESCRIPTION_CSS + '<div class="container-fluid">' + html + '</div>' + settings.EBAY_ITEM_DESCRIPTION_JS

def get_policy_for_ebay_item_description():
    return  """<div class="container-fluid">
    <br/>
    <hr/>
    <br/>
    <div class="panel panel-rfi">
        <div class="panel-heading">Shipping information</div>
        <div class="panel-body">
            %s
        </div>
    </div>
    <div class="panel panel-rfi">
        <div class="panel-heading">Payment information</div>
        <div class="panel-body">
            %s
        </div>
    </div>
    <div class="panel panel-rfi">
        <div class="panel-heading">Return policy</div>
        <div class="panel-body">
            %s
        </div>
    </div>
    </div>""" % (settings.EBAY_STORE_DEFAULT_POLICY_SHIPPING, 
        settings.EBAY_STORE_DEFAULT_POLICY_PAYMENT, 
        settings.EBAY_STORE_DEFAULT_POLICY_RETURN)

def take_screenshot(webdriver, filename=None):
    if filename == None:
        filename = str(time.time()) + '.png'

    webdriver.get_screenshot_as_file(os.path.join(os.path.dirname(__file__), os.pardir, 'ss', filename))

def calculate_profitable_price(amazon_item_price, 
    margin_percentage=settings.APP_EBAY_LISTING_MARGIN_PERCENTAGE, 
    max_margin_dollar=settings.APP_EBAY_LISTING_MAX_MARGIN_DOLLAR, 
    include_salestax_on_cost=True):
    """i.e. with 3 percent margin
        
        ((cost * 1.10 * 1.09 + .20) * 1.029 + .30) * 1.03

        - * 1.10:   10 percent sales tax - also changed on amazon.com
        - * 1.09:   9 percent final value fee charged by ebay
        - + .20:    20 cent listing fee charged by ebay
        - * 1.029:  2.9 percent transaction fee charged by paypal
        - + .30:    30 cent transaction fee by paypal
        - * 1.03:   and my 3 percent margin or $2.50 whichever comes less
    """
    
    profitable_price = -1

    try:
        if include_salestax_on_cost:
            cost = (float(amazon_item_price) * 1.10 * 1.09 + 0.20) * 1.029 + 0.30
        else:
            cost = (float(amazon_item_price) * 1.09 + 0.20) * 1.029 + 0.30
        margin_calculated = cost * (float(margin_percentage) / 100)
        actual_margin = margin_calculated if margin_calculated < max_margin_dollar else max_margin_dollar
        
        profitable_price = Decimal(cost + actual_margin).quantize(Decimal('1.00'))

    except Exception:
        logger.exception("Unable to calculate profitable price")

    return profitable_price

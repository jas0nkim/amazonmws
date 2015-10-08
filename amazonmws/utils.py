import urllib2
import os
import time
import json

from decimal import Decimal
from uuid import UUID

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

def dict_to_unicode(dictionary):
    return str(dictionary).decode('unicode-escape')

def dict_to_json_string(dictionary):
    return json.dumps(dictionary, ensure_ascii=False, cls=SpecialTypedJSONEncoder)

def merge_two_dicts(x, y):
    return dict(x.items() + y.items())

def apply_ebay_listing_template(desc):
    html = """<div class="container-fluid">
    <div class="panel panel-rfi">
        <div class="panel-heading">Description</div>
        <div class="panel-body">
            %s
        </div>
    </div>
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
    </div>""" % (desc, 
        settings.EBAY_STORE_DEFAULT_POLICY_SHIPPING, 
        settings.EBAY_STORE_DEFAULT_POLICY_PAYMENT, 
        settings.EBAY_STORE_DEFAULT_POLICY_RETURN)
    
    return settings.EBAY_ITEM_DESCRIPTION_CSS + html + settings.EBAY_ITEM_DESCRIPTION_JS

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

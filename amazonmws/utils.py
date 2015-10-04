import urllib2
from os.path import basename

from .loggers import GrayLogger as logger
from . import settings


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
            <p>All of our products come with free Standard Shipping. Handling time on our orders is between 1-2 business days. We will ship your item out using the most efficient carrier to your area (USPS, UPS, FedEx, Lasership, etc.). Once it has been shipped out, you should be receiving it within 3 - 5 business days. Currently, we only ship to physical addresses located within the 48 contiguous states of America. P.O. boxes, APO/FPO addresses, Alaska and Hawaii are outside of our shipping zone.</p>
        </div>
    </div>
    <div class="panel panel-rfi">
        <div class="panel-heading">payment information</div>
        <div class="panel-body">
            <p>We only accept Paypal. Credit Card Payment Acceptable through PayPal.</p>
        </div>
    </div>
    <div class="panel panel-rfi">
        <div class="panel-heading">return policy</div>
        <div class="panel-body">
            <p>We fully guarantee all of our items. All items are Brand new and unused. 14 days refunds - we accept returns with defective or being pre-authorized. 10 percent restocking fee may apply.  Please contact us to get an authorization and returning address before sending the item back. Please leave a note with your eBay ID along with the returned item. Buyers pay shipping fees at their own cost to return products for exchange or refund. We will be responsible for the postage of replacements sending out.</p>
        </div>
    </div>
    </div>""" % desc
    return settings.EBAY_ITEM_DESCRIPTION_CSS + html + settings.EBAY_ITEM_DESCRIPTION_JS

def get_policy_for_ebay_item_description():
    return  """<div class="container-fluid">
    <br/>
    <hr/>
    <br/>
    <div class="panel panel-rfi">
        <div class="panel-heading">Shipping information</div>
        <div class="panel-body">
            <p>All of our products come with free Standard Shipping. Handling time on our orders is between 1-2 business days. We will ship your item out using the most efficient carrier to your area (USPS, UPS, FedEx, Lasership, etc.). Once it has been shipped out, you should be receiving it within 3 - 5 business days. Currently, we only ship to physical addresses located within the 48 contiguous states of America. P.O. boxes, APO/FPO addresses, Alaska and Hawaii are outside of our shipping zone.</p>
        </div>
    </div>
    <div class="panel panel-rfi">
        <div class="panel-heading">payment information</div>
        <div class="panel-body">
            <p>We only accept Paypal. Credit Card Payment Acceptable through PayPal.</p>
        </div>
    </div>
    <div class="panel panel-rfi">
        <div class="panel-heading">return policy</div>
        <div class="panel-body">
            <p>We fully guarantee all of our items. All items are Brand new and unused. 14 days refunds - we accept returns with defective or being pre-authorized. 10 percent restocking fee may apply.  Please contact us to get an authorization and returning address before sending the item back. Please leave a note with your eBay ID along with the returned item. Buyers pay shipping fees at their own cost to return products for exchange or refund. We will be responsible for the postage of replacements sending out.</p>
        </div>
    </div>
    </div>"""

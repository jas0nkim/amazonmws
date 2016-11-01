import urllib2
import os
import time
import json
import requests
import re
import random
import gc

import RAKE
import math
import datetime

from decimal import Decimal
from uuid import UUID

from xml.sax.saxutils import escape

from PIL import Image
from StringIO import StringIO

from jinja2 import Template

from stem import Signal
from stem.control import Controller

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

    except urllib2.HTTPError as e:
        logger.exception(e)

    except urllib2.URLError as e:
        logger.exception(e)

    return ret

def validate_image_size(url):
    response = requests.get(url)
    try:
        img = Image.open(StringIO(response.content))
    except IOError as e:
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

def str_to_float(string):
    # trim everything except number and dot(.)
    return money_to_float(string)

def extract_amz_order_num(string):
    return re.sub(r'[^\d\-]+', '', string)

def extract_amz_carrier(string):
    return string.replace('Carrier:', '').strip()

def extract_amz_tracking_num(string):
    return string.replace('Tracking #:', '').strip()

def number_to_dcmlprice(number):
    return Decimal(number).quantize(Decimal('1.00'))

def make_nicer_price(number):
    # make price to end with either .99 (i.e. 24.99) or .49 (i.e. 17.49)
    frac, whole = math.modf(number)
    if frac > 0.5:
        return math.ceil(number) - 0.01
    else:
        return math.ceil(number) - 0.51

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

def is_valid_amazon_order_id(string):
    return re.match(settings.AMAZON_ORDER_ID_PATTERN, string)

def extract_seller_id_from_uri(uri):
    match = re.match(r'^.+?(?=seller=)([^&]+).*$', uri)
    if match:
        return match.group(1).replace('seller=', '').strip()
    else:
        return None

def replace_email_to(string, replace_to=''):
    if not string:
        return string
    return re.sub(r'[\w\.-]+@[\w\.-]+', replace_to, string)

def replace_url_to(string, replace_to=''):
    if not string:
        return string
    return re.sub(r'(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})?(/([\w/_\.#-]*(\?\S+)?[^\.\s])?)', replace_to, string)

def clean_ebay_listing_description(string):
    if not string:
        return string
    string = replace_email_to(string, 'here')
    string = replace_url_to(string, 'here')
    # ebay does not like following words on description:
    improper_words = ['amazon', 'coupon', ]
    for iw in improper_words:
        string = re.sub("(?i)" + iw, "", string)
    return string

def apply_ebay_listing_template(amazon_item, ebay_store, description=None):
    if not ebay_store.item_description_template or ebay_store.item_description_template == "":
        template = settings.EBAY_STORE_DEFAULT_ITEM_DESCRIPTION_TEMPLATE
    else:
        template = ebay_store.item_description_template

    t = Template(template)
    description = description if description else amazon_item.description
    return t.render(asin=amazon_item.asin,
        title=amazon_item.title, 
        description=clean_ebay_listing_description(description if description else amazon_item.description),
        features=clean_ebay_listing_description(amazon_item.features),
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

def file_error(filename, content=None):
    if settings.APP_ENV != 'stage':
        return False
    try:
        with open(os.path.join(os.path.dirname(__file__), os.pardir, 'ss', filename), 'w') as error_file:
            error_file.write(str_to_unicode(content).encode('utf-8'))
    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)
    except:
        print "Unexpected error:", sys.exc_info()[0]
    return False

def calculate_profitable_price(amazon_item_price, ebay_store):
    margin_percentage = ebay_store.margin_percentage if ebay_store.margin_percentage != None else settings.APP_EBAY_LISTING_MARGIN_PERCENTAGE
    margin_min_dollar = float(ebay_store.margin_min_dollar) if ebay_store.margin_min_dollar != None else settings.APP_EBAY_LISTING_MARGIN_MIN_DOLLAR
    margin_max_dollar = float(ebay_store.margin_max_dollar) if ebay_store.margin_max_dollar != None else settings.APP_EBAY_LISTING_MARGIN_MAX_DOLLAR
    use_salestax_table = ebay_store.use_salestax_table
    fixed_salestax_percentage = ebay_store.fixed_salestax_percentage

    return _cal_profitable_price(amazon_cost=amazon_item_price,
        margin_percentage=margin_percentage,
        margin_min_dollar=margin_min_dollar,
        margin_max_dollar=margin_max_dollar,
        use_salestax_table=use_salestax_table,
        fixed_salestax_percentage=fixed_salestax_percentage)

def _cal_profitable_price(amazon_cost, margin_percentage, margin_min_dollar, margin_max_dollar, use_salestax_table, fixed_salestax_percentage):
    """i.e. with 5 percent margin
        
        total_cost - (total_cost * 0.09) - 0.20 - (total_cost * 0.045) - 0.30 = amazon_cost * 1.07
        total_cost - 0.20 - 0.30 - (total_cost * (0.09 + 0.045)) = amazon_cost * 1.07
        total_cost - (total_cost * (0.09 + 0.045)) = (amazon_cost * 1.07) + 0.20 + 0.30
        total_cost * (1 - 0.09 - 0.045 - 0.05) = (amazon_cost * 1.07) + 0.20 + 0.30
        total_cost = ((amazon_cost * 1.07) + 0.20 + 0.30) / (1 - 0.09 - 0.045)

        i.e. amazon_cost = 12.22 (my ebay site price = 17.99)

        1. with new calculation method
        total_cost = 13.575 / 0.865
        15.69

        2. with old calculation method
        total_cost = (12.22 * 1.07 * 1.09 + 0.2) * 1.045 + 0.30
        13.90

        - * i.e. 1.07:   7 percent fixed sales tax - also charged on amazon.com
        - * 1.09:   9 percent final value fee charged by ebay
        - + .20:    20 cent listing fee charged by ebay
        - * 1.045:  3.7 percent transaction fee (international) + 0.8 percent cross-border payment charged by paypal
        - + .30:    30 cent transaction fee by paypal
        - * 1.03:   and my 3 percent margin or $2.50 whichever comes less
    """
    
    profitable_price = -1

    try:
        if use_salestax_table:
            total_cost = (float(amazon_cost) + 0.20 + 0.30) / (1.00 - 0.09 - 0.045)
        else:
            total_cost = (float(amazon_cost) * (1.0 + float(fixed_salestax_percentage) / 100) + 0.20 + 0.30) / (1.00 - 0.09 - 0.045)
        margin_calculated = total_cost * (float(margin_percentage) / 100)
        actual_margin = margin_calculated if margin_min_dollar < margin_calculated and margin_calculated < margin_max_dollar else margin_min_dollar if margin_calculated <= margin_min_dollar else margin_max_dollar
        
        profitable_price = number_to_dcmlprice(make_nicer_price(total_cost + actual_margin))

    except Exception:
        logger.exception("Unable to calculate profitable price")

    return profitable_price

def check_lock(filename, max_age_hours=6):
    MAX_AGE_IN_SECS = 60 * 60 * max_age_hours # 6 hours sitting max
    lock_file = os.path.join(settings.LOCK_PATH, filename)
    if os.path.isfile(lock_file):
        # avoid process killed - and lockfile sitting around...
        if os.time.time() - os.path.getmtime(lock_file) > MAX_AGE_IN_SECS:
            logger.info('[%s] Lock file sitting around more than maximum hours [%d]. Delete the lock and start new process.' % (filename, max_age_hours))
            release_lock(filename)
            check_lock(filename, max_age_hours)
        else:
            # this script is running by other process - so exit
            die_message = '[%s] A task is still running by other process. Ending this process.' % filename
            logger.info(die_message)
            raise Exception(die_message)
    else:
        open(lock_file, 'w')
        logger.info('[%s] Lock file created' % lock_file)

def release_lock(filename):
    lock_file = os.path.join(settings.LOCK_PATH, filename)
    if os.path.isfile(lock_file):
        os.remove(lock_file)
        logger.info('[%s] Lock file removed' % lock_file)

def to_keywords(string):
    if not string:
        return []
    Rake = RAKE.Rake(os.path.join(settings.APP_PATH, 'rake', 'stoplists', 'SmartStoplist.txt'));
    keywords = Rake.run(re.sub(r'([^\s\w]|_)+', ' ', string).strip());
    if len(keywords) > 0:
        return keywords[0][0].split()
    return []

def renew_tor_connection(sleep=settings.TOR_DEFAULT_SLEEP):
    """ sleep: in seconds
    """
    with Controller.from_port(port=settings.TOR_CONTROLPORT_LISTENER_PORT) as controller:
        # TOR: Rate limiting NEWNYM request: delaying by 10 second(s)
        # ref: http://stackoverflow.com/a/8337748
        # force to sleep , i.e. 3 seconds, each
        time.sleep(sleep)
        controller.authenticate(password=settings.TOR_PASSWORD)
        controller.signal(Signal.NEWNYM)

def add_check_digit(upc_str):
    """
    ref: https://gist.github.com/corpit/8204593

    Returns a 12 digit upc-a string from an 11-digit upc-a string by adding 
    a check digit

    >>> add_check_digit('02345600007')
    '023456000073'
    >>> add_check_digit('21234567899')
    '212345678992'
    >>> add_check_digit('04210000526')
    '042100005264'
    """

    upc_str = str(upc_str)
    if len(upc_str) != 11:
        raise Exception("Invalid length")

    odd_sum = 0
    even_sum = 0
    for i, char in enumerate(upc_str):
        j = i+1
        if j % 2 == 0:
            even_sum += int(char)
        else:
            odd_sum += int(char)

    total_sum = (odd_sum * 3) + even_sum
    mod = total_sum % 10
    check_digit = 10 - mod
    if check_digit == 10:
        check_digit = 0
    return upc_str + str(check_digit)

def get_upc(specs=[]):
    if len(specs) > 0:
        for spec in specs:
            for key, val in spec.iteritems():
                if key == 'UPC':
                    return val
    return add_check_digit(str(random.choice([0, 1, 6, 7, 8])) + str(random.randint(1000000000, 9999999999)))

def get_ean(upc=None):
    if upc:
        return str(0) + str(upc)
    else:
        return None

def get_mpn(specs=[]):
    if len(specs) > 0:
        for spec in specs:
            for key, val in spec.iteritems():
                if key == 'Item model number':
                    return val
    """
    set random string (int between 7 - 11 digit) for now
    """
    return str(random.randint(2000000, 79999999999))

def build_ebay_product_listing_details(brand=None, mpn=None, upc=None):
    product_listing_details = {
        ### Legacy
        #
        # "BrandMPN": {
        #     "Brand": "",
        #     "MPN": "",
        # },
        "UPC": "",
    }
    # product_listing_details['BrandMPN']['Brand'] = xml_escape(brand)
    # product_listing_details['BrandMPN']['MPN'] = xml_escape(mpn)
    product_listing_details['UPC'] = xml_escape(upc)
    return product_listing_details

def build_ebay_item_specifics(brand=None, mpn=None, upc=None, other_specs=[]):
    name_value_list = []
    if brand:
        brand = xml_escape(brand)
        name_value_list.append({
            'Name': 'Brand',
            'Value': brand,
        })
    if mpn:
        mpn = xml_escape(mpn)
        name_value_list.append({
            'Name': 'Model',
            'Value': mpn,
        })
        name_value_list.append({
            'Name': 'MPN',
            'Value': mpn,
        })
    if upc:
        upc = xml_escape(upc)
        name_value_list.append({
            'Name': 'UPC',
            'Value': upc,
        })
        name_value_list.append({
            'Name': 'EAN',
            'Value': get_ean(upc=upc),
        })
    if len(other_specs) > 0:
        for other_spec in other_specs:
            for key, val in other_spec.iteritems():
                if key == 'Product Dimensions':
                    name_value_list.append({
                        'Name': 'Dimensions',
                        'Value': xml_escape(val),
                    })
                elif key == 'Item Weight':
                    name_value_list.append({
                        'Name': 'Weight',
                        'Value': xml_escape(val),
                    })
                elif key == 'Color':
                    name_value_list.append({
                        'Name': 'Color',
                        'Value': xml_escape(val),
                    })
                else:
                    continue
    return { "NameValueList": name_value_list }

# ref: http://stackoverflow.com/a/3368991
def find_between(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]

    except ValueError:
        return ""

def xml_escape(string):
    if string is None:
        return ''
    return escape(string)

def generate_ebay_item_title(source_title):
    source_title = re.sub("like", "", source_title, flags=re.I) # ebay does now allow word 'like' in item title
    source_title = xml_escape(source_title.strip())
    add_dots = False
    if len(source_title) > 80:
        source_title = source_title[:77]
        if source_title.rsplit(' ', 1)[1].startswith('&') and not source_title.rsplit(' ', 1)[1].endswith(';'):
            # remove an incompleted escaped string at the end
            source_title = source_title.rsplit(' ', 1)[0]
        add_dots = True
    return source_title if not add_dots else source_title + '...'

def generate_ebay_store_category_name(source_category_name):
    source_category_name = xml_escape(source_category_name.strip())
    return source_category_name if len(source_category_name) < 30 else source_category_name[:27] + '...'

def queryset_iterator(queryset, chunksize=1000):
    '''''
    Iterate over a Django Queryset ordered by the primary key

    This method loads a maximum of chunksize (default: 1000) rows in it's
    memory at the same time while django normally would load all rows in it's
    memory. Using the iterator() method only causes it to not preload all the
    classes.

    Note that the implementation of the iterator does not support ordered query sets.
    '''
    if queryset.count() > 0:
        pk = 0
        last_pk = queryset.order_by('-pk')[0].pk
        queryset = queryset.order_by('pk')
        while pk < last_pk:
            for row in queryset.filter(pk__gt=pk)[:chunksize]:
                pk = row.pk
                yield row
            gc.collect()

def replace_html_anchors_to_spans(unicoded_html):
    # /(<a[^>]*>)([^<]+)(</a>)/
    return re.sub(r'(<a[^>]*>)([^<]+)(</a>)', lambda m: u'<span class="link-replacement">' + m.group(2) + u'</span>', unicoded_html)

def convert_to_ebay_shoe_variation_name(gender_type):
    return "US Shoe Size (" + gender_type.title() + "'s)"

def convert_amazon_category_name_to_list(amazon_category, delimiter=':'):
    return [ c.strip() for c in amazon_category.split(delimiter) ]

def get_utc():
    ZERO = datetime.timedelta(0)
    class UTC(datetime.tzinfo):
      def utcoffset(self, dt):
        return ZERO
      def tzname(self, dt):
        return "UTC"
      def dst(self, dt):
        return ZERO
    return UTC()

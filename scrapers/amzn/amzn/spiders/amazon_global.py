import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))

from scrapy import Request
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.link import Link

from amazonmws import settings as amazonmws_settings, utils as amazonmws_utils
from amzn.spiders import AmazonKeywordSearchSpider
from amzn import parsers


class AmazonGlobalSpider(AmazonKeywordSearchSpider):
    
    name = "amazon_global"

    international_shipping = True

    def __init__(self, *a, **kw):
        super(AmazonGlobalSpider, self).__init__(*a, **kw)
        if 'international_shipping' in kw:
            self.international_shipping = kw['international_shipping']

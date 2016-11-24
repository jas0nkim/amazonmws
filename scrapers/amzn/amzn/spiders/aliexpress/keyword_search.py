import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..'))

import urlparse

from urllib import urlencode

from scrapy import Request
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.link import Link

from amazonmws import settings as amazonmws_settings, utils as amazonmws_utils
from amzn.spiders import AliexpressBaseSpider
from amzn import parsers


class AliexpressKeywordSearchSpider(AliexpressBaseSpider):
    
    name = "aliexpress_keyword_search"

    rules = [
        # Extract amazon item links under main result section
        Rule(LinkExtractor(allow=[amazonmws_settings.ALIEXPRESS_ITEM_LINK_PATTERN],
                restrict_css=['div.list-items ul li.list-item']),
            callback=parsers.parse_aliexpress_item,
            process_links='filter_item_links',
            process_request='pre_item_request',
            follow=True
        ),
    ]

    max_page = None

    def __init__(self, *a, **kw):
        super(AliexpressKeywordSearchSpider, self).__init__(*a, **kw)
        if 'max_page' in kw:
            self.max_page = kw['max_page']

    def parse_start_url(self, response):
        if response.status != 200:
            return None
        p_num = 1
        u = urlparse.urlparse(response.url)
        qs = urlparse.parse_qs(u.query)
        if 'page' in qs:
            # remove 'page' query from url in order to replace to the next page.
            p_num = int(qs.pop('page', None)[0])
            u._replace(query=urlencode(qs, True))
        if self.max_page and self.max_page < p_num + 1:
            return None
        return Request("{}&page={}".format(u.geturl(), p_num + 1))

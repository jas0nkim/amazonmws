import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))

from scrapy import Request
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.link import Link

from amazonmws import settings as amazonmws_settings, utils as amazonmws_utils
from amzn.spiders import AmazonBaseSpider
from amzn import parsers


class AmazonKeywordSearchSpider(AmazonBaseSpider):
    
    name = "amazon_keyword_search"

    rules = [
        # Extract amazon item links under main result section
        Rule(LinkExtractor(allow=[amazonmws_settings.AMAZON_ITEM_LINK_PATTERN],
                restrict_css=['ul.s-result-list li.s-result-item']),
            callback=parsers.parse_amazon_item,
            process_links='filter_item_links',
            process_request='pre_item_request',
            follow=True
        ),
    ]

    max_page = None

    def __init__(self, *a, **kw):
        super(AmazonKeywordSearchSpider, self).__init__(*a, **kw)
        if 'max_page' in kw:
            self.max_page = kw['max_page']

    def parse_start_url(self, response):
        if "&page=" not in response.url:
            last_page = None
            if len(response.css('#pagn .pagnDisabled::text')) > 0:
                last_page = int(response.css('#pagn .pagnDisabled::text')[0].extract().strip())
            elif len(response.css('#pagn .pagnLink a::text')) > 0:
                last_page = int(response.css('#pagn .pagnLink a::text')[-1].extract().strip())
            else:
                last_page = 1

            if self.max_page and self.max_page < last_page:
                last_page = self.max_page

            for i in range(1, last_page + 1):
                yield Request("{}&page={}".format(response.url, i))

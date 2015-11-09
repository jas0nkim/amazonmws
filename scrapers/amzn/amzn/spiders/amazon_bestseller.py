import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))

import re

from scrapy import Request
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

from amazonmws import settings as amazonmws_settings
from amzn.spiders import AmazonBaseSpider
from amzn import parsers


class AmazonBestsellerSpider(AmazonBaseSpider):
    
    name = "amazon_bestseller"

    rules = [
        # Extract all links under category section
        Rule(LinkExtractor(allow=[r'.*'],
                restrict_css=['ul#zg_browseRoot li:not(.zg_browseUp)']),
            callback=parsers.parse_amazon_bestseller,
            process_links='filter_category_links',
            follow=True
        ),

        # Extract page links under each categories
        Rule(LinkExtractor(allow=[r'.*'],
                restrict_css=['#zg_paginationWrapper li.zg_page']),
            callback=parsers.parse_amazon_bestseller,
            process_links='filter_page_links',
            follow=True
        ),
    ]

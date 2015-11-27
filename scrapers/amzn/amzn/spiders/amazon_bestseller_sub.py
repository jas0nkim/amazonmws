import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))

import re

from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.link import Link

from amzn.spiders import AmazonBaseSpider
from amzn import parsers


class AmazonBestsellerSubSpider(AmazonBaseSpider):
    
    name = "amazon_bestseller_sub"

    rules = [
        # Extract all links under category section
        Rule(LinkExtractor(allow=[r'.*'],
                restrict_css=['ul#zg_browseRoot li:not(.zg_browseUp)']),
            callback=parsers.parse_amazon_bestseller,
            process_links='filter_category_links',
            follow=True
        ),
    ]

    def filter_category_links(self, links):
        filtered_links = []
        for link in links:
            striped_link_url = re.sub(r'(ref=.*)$', '', link.url)
            if striped_link_url not in self._category_links_cache:
                self._category_links_cache[striped_link_url] = True
                for i in range (1, 6): # append page links here
                    paged_link = Link('%s?_encoding=UTF8&pg=%d' % (striped_link_url, i), 
                        link.text, link.fragment, link.nofollow)
                    filtered_links.append(paged_link)
        return filtered_links

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class AmazonListingSpider(CrawlSpider):
    
    name = "amazon_listing"

    allowed_domains = ["amazon.com"]
    start_urls = [
        'http://www.amazon.com/b?ie=UTF8&node=12896641',
    ]

    rules = [
        # Extract all links under category section
        Rule(LinkExtractor(allow=[r'.*'],
                restrict_css=['#refinements .categoryRefinementsSection ul li:not(.shoppingEngineExpand)']),
            callback='parse_category',
            follow=True
        ),

        # Extract amazon item links under main result section
        Rule(LinkExtractor(allow=[r'^https?://www.amazon.com/([^/]+)/([^/]+)/([A-Z0-9]{10})(/.*$)?'],
                restrict_css=['ul.s-result-list li.s-result-item']),
            callback='parse_item',
            follow=True
        ),
    ]

    def parse_category(self, response):
        # print "hello"
        print "category - " + response.url
        # print "world"
        # pass

    def parse_item(self, response):
        print "item - " + response.url

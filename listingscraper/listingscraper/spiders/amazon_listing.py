from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class AmazonListingSpider(CrawlSpider):
    
    name = "amazon_listing"

    allowed_domains = ["amazon.com"]
    start_urls = [
        'http://www.amazon.com/b?ie=UTF8&node=12896641',
    ]

    __page_links_cache = {}

    rules = [
        # Extract all links under category section
        Rule(LinkExtractor(allow=[r'.*'],
                restrict_css=['#refinements .categoryRefinementsSection ul li:not(.shoppingEngineExpand)']),
            callback='parse_category',
            follow=True
        ),

        # Extract page links under each categories
        Rule(LinkExtractor(allow=[r'.*'],
                restrict_css=['#pagn .pagnLink']),
            callback='parse_page',
            process_links='filter_page_links',
            follow=True
        ),

        # Extract amazon item links under main result section
        Rule(LinkExtractor(allow=[r'^https?://www.amazon.com/([^/]+)/([^/]+)/([A-Z0-9]{10})(/.*$)?'],
                restrict_css=['ul.s-result-list li.s-result-item']),
            callback='parse_item',
            process_links='filter_item_links',
            follow=True
        ),
    ]

    def filter_page_links(self, links):
        filtered_links = []
        for link in links:
            if link.url not in self.__page_links_cache:
                self.__page_links_cache[link.url] = True
                filtered_links.append(link)
        return filtered_links

    def filter_item_links(self, links):
        pass

    def parse_category(self, response):
        print "category - " + response.url

    def parse_page(self, response):
        print "page - " + response.url

    def parse_item(self, response):
        print "item - " + response.url


import datetime

from scrapy.http import Request

from storm.exceptions import StormError

from amazonmws.spiders.keywords_spider import KeywordsSpider
from amazonmws.models import Scraper, Lookup, StormStore

class DblookupSpider(KeywordsSpider):
    """DblookupSpider

    A spider to discover items by lookup database table

    """
    name = "keywords_dblookup"
    SCRAPER_ID = Scraper.amazon_keywords_dblookup
    current_lookup_id = None

    def start_requests(self):
        """override
        """
        lookups = StormStore.find(Lookup)
        if lookups.count() > 0:
            for lookup in lookups:
                self.current_lookup_id = lookup.id
                yield Request(lookup.url, self.parse)

    def __add_lookup_relationship(self, amazon_item):
        try:
            relationship = LookupAmazonItem()
            relationship.lookup_id = self.current_lookup_id
            relationship.amazon_item_id = amazon_item.id
            relationship.created_at = datetime.datetime.now()
            relationship.updated_at = datetime.datetime.now()

            StormStore.add(relationship)
            StormStore.commit()

        except StormError, e:
            logger.exception("[ASIN: " + amazon_item.asin + "] " + "Failed to link with lookup id: " + str(relationship.lookup_id))
            StormStore.rollback()


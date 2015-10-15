import datetime

from scrapy.http import Request

from storm.exceptions import StormError

from amazonmws import utils
from amazonmws.spiders.keywords_spider import KeywordsSpider
from amazonmws.models import Scraper, Lookup, StormStore


class KeywordsDblookupSpider(KeywordsSpider):
    """KeywordsDblookupSpider

    A spider to discover items by lookup database table

    """
    name = "keywords_dblookup"
    SCRAPER_ID = Scraper.amazon_keywords_dblookup
    lookup_ids = []
    lookup_id_index = 0

    current_lookup_id = None

    def __init__(self):
        KeywordsSpider.__init__(self)
        lookups = StormStore.find(Lookup, Lookup.spider_name == utils.str_to_unicode(self.name))
        if lookups.count() > 0:
            for lookup in lookups:
                self.start_urls.append(lookup.url)
                self.lookup_ids.append(lookup.id)

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


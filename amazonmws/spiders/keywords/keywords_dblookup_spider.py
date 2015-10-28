import datetime

from scrapy.http import Request

from storm.exceptions import StormError

from amazonmws import utils
from amazonmws.spiders.keywords_spider import KeywordsSpider
from amazonmws.models import Scraper, Lookup, StormStore
from amazonmws.loggers import GrayLogger as logger, StaticFieldFilter, get_logger_name


class KeywordsDblookupSpider(KeywordsSpider):
    """KeywordsDblookupSpider

    A spider to discover items by lookup database table

    """
    name = "keywords_dblookup"
    SCRAPER_ID = Scraper.amazon_keywords_dblookup
    lookups = None

    start_urls = ['http://www.amazon.com']

    def __init__(self, lookup_id=None):
        KeywordsSpider.__init__(self)
        if lookup_id != None:
            lookups = StormStore.find(Lookup, 
                Lookup.spider_name == utils.str_to_unicode(self.name),
                Lookup.id == int(lookup_id))
        else:
            lookups = StormStore.find(Lookup, Lookup.spider_name == utils.str_to_unicode(self.name))
        
        if lookups.count() > 0:
            self.lookups = lookups

    def __add_lookup_relationship(self, amazon_item, current_lookup_id):
        try:
            relationship = LookupAmazonItem()
            relationship.lookup_id = current_lookup_id
            relationship.amazon_item_id = amazon_item.id
            relationship.created_at = datetime.datetime.now()
            relationship.updated_at = datetime.datetime.now()

            StormStore.add(relationship)
            StormStore.commit()

        except StormError, e:
            logger.exception("[ASIN: " + amazon_item.asin + "] " + "Failed to link with lookup id: " + str(relationship.lookup_id))
            StormStore.rollback()


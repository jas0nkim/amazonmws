from amazonmws.spiders.keywords_spider import KeywordsSpider
from amazonmws.models import Scraper


class KidscustumeSpider(KeywordsSpider):
    """KidscustumeSpider

    A spider to discover items by keywords - custume - from amazon.com site

    """
    name = "keywords_kidscustume"
    start_urls = [
        # Best Sellers - Toys and Games
        "http://www.amazon.com/s/ref=sr_ex_n_8?rh=n%3A7141123011%2Cn%3A7586165011%2Cn%3A721068011%2Cn%3A2229578011&bbn=721068011&ie=UTF8&qid=1443730551",
        "http://www.amazon.com/s/ref=lp_721070011_ex_n_7?rh=n%3A7141123011%2Cn%3A7586165011%2Cn%3A721070011%2Cn%3A2229581011&bbn=721070011&ie=UTF8&qid=1443731015",
        "http://www.amazon.com/gp/search/ref=sr_ex_n_9?rh=n%3A7141123011%2Cn%3A7586165011%2Cn%3A721067011%2Cn%3A2229575011&bbn=721067011&ie=UTF8&qid=1443731030",
    ]
    
    SCRAPER_ID = Scraper.amazon_keywords_kidscustume

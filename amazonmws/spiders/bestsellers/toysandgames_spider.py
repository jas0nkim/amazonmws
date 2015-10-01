from amazonmws.spiders.best_sellers_spider import BestSellersSpider
from amazonmws.models import Scraper


class ToysandgamesSpider(BestSellersSpider):
    """ToysandgamesSpider

    A spider to discover best seller items under Toys and Games from amazon.com site - sub-directories of http://www.amazon.com/Best-Sellers/zgbs

    """
    name = "bestsellers_toysandgames"
    start_urls = [
        # Best Sellers - Toys and Games
        "http://www.amazon.com/Best-Sellers-Toys-Games/zgbs/toys-and-games",
    ]
    
    SCRAPER_ID = Scraper.amazon_bestsellers_toyandgames

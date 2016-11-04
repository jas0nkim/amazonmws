# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

from amazon_asin import AmazonAsinSpider
from amazon_base import AmazonBaseSpider
from amazon_pricewatch import AmazonPricewatchSpider
from amazon_pricewatch_variation_specific import AmazonPricewatchVariationSpecificSpider
from amazon_bestseller import AmazonBestsellerSpider
from amazon_keyword_search import AmazonKeywordSearchSpider
from amazon_global import AmazonGlobalSpider

# legacy Spiders
from amazon_apparels import AmazonApparelSpider
from amazon_asin_offers import AmazonAsinOffersSpider

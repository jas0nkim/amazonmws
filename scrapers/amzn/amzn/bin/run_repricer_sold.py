import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging

from amazonmws import utils as amazonmws_utils
from amazonmws.loggers import set_root_graylogger, GrayLogger as logger
from amazonmws.model_managers import *


if __name__ == "__main__":
    # configure_logging(install_root_handler=False)
    # set_root_graylogger()

    from amazonmws import django_cli
    django_cli.execute()

    asins = []
    for tran in TransactionModelManager.fetch():
        ebay_item = EbayItemModelManager.fetch_one(ebid=tran.item_id)
        if not ebay_item:
            continue
        amazon_item = AmazonItemModelManager.fetch_one(ebay_item.asin)
        if not amazon_item:
            continue
        if not amazon_item.asin in asins:
            asins.append(amazon_item.asin)

    process = CrawlerProcess(get_project_settings())
    process.crawl('amazon_asin', asins=asins)
    process.start()


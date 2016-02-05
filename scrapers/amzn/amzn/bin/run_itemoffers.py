import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))

from amazonmws import django_cli
django_cli.execute()

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging

from django.db.models import Max

from amazonmws.loggers import set_root_graylogger, GrayLogger as logger
from amazonmws.model_managers import *


if __name__ == "__main__":
    # configure_logging(install_root_handler=False)
    # set_root_graylogger()

    items = AmazonItemModelManager.fetch()
    if items.count() < 0:
        raise Exception('No amazon items found')

    revision = None
    try:
        revision = AmazonItemOfferModelManager.fetch().aggregate(Max('revision'))['revision__max']
    except Exception as e:
        logger.exception(e)
        revision = None

    if revision == None:
        revision = 0

    revision += 1
    if items.count() > 0:
        process = CrawlerProcess(get_project_settings())
        process.crawl('amazon_asin_offers', asins=[x.asin for x in items], revision=revision)
        process.start()
    else:
        logger.error('No amazon items found')

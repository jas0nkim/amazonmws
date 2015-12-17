import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging

from amazonmws import settings as amazonmws_settings, utils as amazonmws_utils
from amazonmws.loggers import set_root_graylogger, GrayLogger as logger


if __name__ == "__main__":
    # configure_logging(install_root_handler=False)
    # set_root_graylogger()

    asins = [
        u'B00LDGV15I',
        u'B002M9D4HI',
        u'B00P1HU2WI',
        u'B013WBBJF8',
        u'B00EZTCW94',
        u'B00UAHKCWE',
        u'B00VDVW9YK',
        u'B004Y6BH6W',
        u'B000J09OLM',
        u'B00UW2SP80',
        u'B00GNB3MRI',
        u'B0072H60MG',
        u'B0013JPVN8',
        u'B00D5P846Y',
        u'B00KG6Z972',
        u'B00QCAGVFA',
        u'B00U9RWQMY',
        u'B001W2WKS0',
        u'B00JCW8D38',
        u'B00QPHW63G',
        u'B00GJMYDK6',
        u'B00RQLC7GQ',
        u'B002M782UO',
        u'B00Y2BGFIO',
        u'B00LD6UCCG',
        u'B00KWR2BCQ',
        u'B00MUZVKY8',
    ]

    process = CrawlerProcess(get_project_settings())
    process.crawl('amazon_asin', asins=asins)
    process.start()


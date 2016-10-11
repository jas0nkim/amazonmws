import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'scrapers', 'amzn'))

import getopt

from amazonmws import django_cli
django_cli.execute()

from amazonmws import settings as amazonmws_settings, utils as amazonmws_utils
from amazonmws.loggers import GrayLogger as logger
from amazonmws.model_managers import *


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "h:")
    except getopt.GetoptError:
        print 'hotfix_amazon_order_items.py'
        sys.exit(2)
    
    for opt, arg in opts:
        if opt == '-h':
            print 'hotfix_amazon_order_items.py'
            sys.exit()
    run()

def run():
    _cache = {}

    for amazon_order in amazonmws_utils.queryset_iterator(AmazonOrderModelManager.fetch()):
        try:
            AmazonOrderItemModelManager.create(amazon_order=amazon_order,
                order_id=amazon_order.order_id,
                asin=amazon_order.asin,
                is_variation=False)
        except Exception as e:
            print("[" + amazon_order.asin + "] " + str(e))
            logger.exception("[ASIN:" + amazon_order.asin + "] " + str(e))


if __name__ == "__main__":
    main(sys.argv[1:])

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
        print 'hotfix_ebay_item_stats_ebay_store_id.py'
        sys.exit(2)
    
    for opt, arg in opts:
        if opt == '-h':
            print 'hotfix_ebay_item_stats_ebay_store_id.py'
            sys.exit()
    run()

def run():
    _cache = {}

    for stats in amazonmws_utils.queryset_iterator(EbayItemStatModelManager.fetch()):
        try:
            logger.debug("[working on EBID:" + stats.ebid + "]")
            if stats.ebid not in _cache:
                ebay_item = EbayItemModelManager.fetch_one(ebid=stats.ebid)
                if stats.ebay_store_id != ebay_item.ebay_store_id:
                    stats.ebay_store_id = ebay_item.ebay_store_id
                    stats.save()
                _cache[stats.ebid] = stats.ebay_store_id
            else:
                if stats.ebay_store_id != _cache[stats.ebid]:
                    stats.ebay_store_id = _cache[stats.ebid]
                    stats.save()
        except Exception as e:
            logger.exception("[EBID:" + stats.ebid + "] " + str(e))


if __name__ == "__main__":
    main(sys.argv[1:])

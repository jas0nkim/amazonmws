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
    ebay_item_stats = amazonmws_utils.queryset_iterator(EbayItemStatModelManager.fetch())

    for each in ebay_item_stats:
        try:
            logger.debug("[working on EBID:" + each.ebid + "]")
            if each.ebid not in _cache:
                ebay_item = EbayItemModelManager.fetch_one(ebid=each.ebid)
                each.ebay_store_id = ebay_item.ebay_store_id
                each.save()
                _cache[each.ebid] = each.ebay_store_id
            else:
                each.ebay_store_id = _cache[each.ebid]
                each.save()
        except Exception as e:
            logger.exception("[EBID:" + each.ebid + "] " + str(e))


if __name__ == "__main__":
    main(sys.argv[1:])

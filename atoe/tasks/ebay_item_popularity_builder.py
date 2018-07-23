import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'scrapers', 'amzn'))

import getopt

from amazonmws import django_cli
django_cli.execute()

from amazonmws import settings as amazonmws_settings, utils as amazonmws_utils
from amazonmws.loggers import GrayLogger as logger
from amazonmws.model_managers import *


__ebay_stores = [1, 8]

__days_as_new_item = 10

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "h:")
    except getopt.GetoptError:
        print 'ebay_item_popularity_builder.py'
        sys.exit(2)
    
    for opt, arg in opts:
        if opt == '-h':
            print 'ebay_item_popularity_builder.py'
            sys.exit()
    run()


def __get_indexers(total):
    """
        return list
        i.e.:
            [1000, 4000]
             # [popular, normal]
             # remove the last - slow - we don't need it
    """
    ret = []
    indexer = 0
    while indexer < len(amazonmws_settings.EBAY_ITEM_POPULARITY_PERCENTAGES) - 1:
        percentage = amazonmws_settings.EBAY_ITEM_POPULARITY_PERCENTAGES[indexer]['percentage']
        if indexer > 0:
            ret.append(int(total * percentage / 100) + ret[indexer - 1])
        else:
            ret.append(int(total * percentage / 100))
        indexer += 1
    return ret


def __get_popularity(row_index, indexers, is_new):
    try:
        # give advantages for new listings
        if int(is_new) == 1 and int(row_index) >= indexers[amazonmws_settings.DEFAULT_EBAY_ITEM_POPULARITY - 1]:
            return amazonmws_settings.DEFAULT_EBAY_ITEM_POPULARITY

        pop = 1
        for _indexer in indexers:
            if int(row_index) <= int(_indexer):
                return pop
            pop += 1
        return amazonmws_settings.DEFAULT_EBAY_ITEM_POPULARITY
    except Exception as e:
        logger.error("failed getting popularity - {}".format(str(e)))
        return amazonmws_settings.DEFAULT_EBAY_ITEM_POPULARITY

def __proceed_with_performance_data(ebay_store):
    performance_data = EbayItemStatModelManager.fetch_performances_past_days(
        ebay_store_id=ebay_store.id,
        days=10,
        order_by='clicks',
        desc=True,
        days_as_new_item=__days_as_new_item)
    total_rows = len(performance_data)
    indexers = __get_indexers(total_rows)
    print("[{}] TOTAL ROWS: {}".format(ebay_store.username, total_rows))
    print("[{}] INDEXERS: {}".format(ebay_store.username, str(indexers)))
    for ebid, curr_clicks, curr_watches, curr_solds, past_clicks, past_watches, past_solds, diff_clicks, diff_watches, diff_solds, new_entry, parent_asin, row_index in performance_data:
        try:
            popularity = __get_popularity(row_index=row_index, indexers=indexers, is_new=new_entry)
            p = EbayItemPopularityModelManager.fetch_one(ebid=ebid)
            if p:
                EbayItemPopularityModelManager.update(pop=p, popularity=popularity)
            else:
                EbayItemPopularityModelManager.create(ebay_store=ebay_store,
                    ebid=ebid,
                    parent_asin=parent_asin,
                    popularity=popularity)
        except Exception as e:
            logger.exception("[EBID:" + ebid + "] " + str(e))

def run():
    """
        popular items - Top 30%
        normal items - Next 40%
        slow items - Next 30%
    """
    for ebay_store_id in __ebay_stores:
        ebay_store = EbayStoreModelManager.fetch_one(id=ebay_store_id)
        if not ebay_store:
            continue
        __proceed_with_performance_data(ebay_store=ebay_store)
    # lastly remove deleted/inactive ebay items
    EbayItemPopularityModelManager.gc()

if __name__ == "__main__":
    main(sys.argv[1:])

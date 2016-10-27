import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'scrapers', 'amzn'))

import getopt

from amazonmws import django_cli
django_cli.execute()

from amazonmws import settings as amazonmws_settings, utils as amazonmws_utils
from amazonmws.loggers import GrayLogger as logger
from amazonmws.model_managers import *


__ebay_stores = [1, 5, 6, 7]

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


def __get_counters(count):
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
        ret.append(int(count * percentage / 100))
        indexer += 1
    return ret


def __proceed_with_new_items(ebay_store):
    # enter new entries - all to normal popularities
    for ebay_store_id, ebid, asin in EbayItemModelManager.fetch_simpleformat(created_at__gt=datetime.datetime.now(tz=amazonmws_utils.get_utc()) - datetime.timedelta(days=10)):
        try:
            p = EbayItemPopularityModelManager.fetch_one(ebid=ebid)
            if p:
                EbayItemPopularityModelManager.update(pop=p, popularity=2)
            else:
                EbayItemPopularityModelManager.create(ebay_store=ebay_store,
                    ebid=ebid,
                    parent_asin=asin,
                    popularity=2)
        except Exception as e:
            logger.exception("[EBID:" + ebid + "] " + str(e))


def __proceed_with_performance_data(ebay_store):
    performance_data = EbayItemStatModelManager.fetch_performances_past_days(
        ebay_store_id=ebay_store.id,
        days=7,
        order_by='clicks',
        desc=True,
        ignore_new_items=True)
    counters = __get_counters(len(performance_data))
    try:
        current_counter = counters.pop(0)
    except IndexError:
        current_counter = None
    popularity = 1
    # enter existing(old) entries
    for table_id, ebid, curr_clicks, curr_watches, curr_solds, past_clicks, past_watches, past_solds, diff_clicks, diff_watches, diff_solds, new_entry in performance_data:
        try:
            p = EbayItemPopularityModelManager.fetch_one(ebid=ebid)
            if p:
                EbayItemPopularityModelManager.update(pop=p, popularity=popularity)
            else:
                ebay_item = EbayItemModelManager.fetch_one(ebid=ebid)
                parent_asin = None
                if ebay_item:
                    parent_asin = ebay_item.asin
                EbayItemPopularityModelManager.create(ebay_store=ebay_store,
                    ebid=ebid,
                    parent_asin=parent_asin,
                    popularity=popularity)
        except Exception as e:
            logger.exception("[EBID:" + ebid + "] " + str(e))

        if current_counter is not None:
            if current_counter > 0:
                current_counter -= 1
            else:
                # next popularity level. reset index
                popularity += 1
                try:
                    current_counter = counters.pop(0)
                except IndexError:
                    current_counter = None

def run():
    """
        - all new entries (inserted during last 10 days) are all normal items. - give padding (suppose to be 7 days)
        - from old entries (inserted more than 10 (7) days ago)
        popular items - Top 10%
        normal items - Next 40%
        slow items - Next 50%
    """
    for ebay_store_id in __ebay_stores:
        ebay_store = EbayStoreModelManager.fetch_one(id=ebay_store_id)
        if not ebay_store:
            continue
        __proceed_with_new_items(ebay_store=ebay_store)
        __proceed_with_performance_data(ebay_store=ebay_store)
    # lastly remove deleted/inactive ebay items
    EbayItemPopularityModelManager.gc()

if __name__ == "__main__":
    main(sys.argv[1:])

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'scrapers', 'amzn'))

import getopt

from amazonmws import django_cli
django_cli.execute()

from amazonmws import settings as amazonmws_settings, utils as amazonmws_utils
from amazonmws.loggers import GrayLogger as logger
from amazonmws.model_managers import *

from atoe.actions import EbayItemAction

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
    """
    return [int(count * 0.1), int(count * 0.4)]

def run():
    """
        popular items - Top 10%
        normal items - Next 40%
        slow items - Next 50%
    """
    for ebay_store_id in __ebay_stores:
        performance_data = EbayItemStatModelManager.fetch_performances_past_days(
            ebay_store_id=ebay_store_id,
            days=7,
            order_by='clicks',
            desc=True)

        counters = __get_counters(len(performance_data))
        popularity = 1
        try:
            current_counter = counters.pop(0)
        except IndexError:
            current_counter = None

        for table_id, ebid, curr_clicks, curr_watches, curr_solds, past_clicks, past_watches, past_solds, diff_clicks, diff_watches, diff_solds in performance_data:
            try:
                EbayItemPopularityModelManager.create(ebay_store=ebay_item.ebay_store,
                    ebid=ebay_item.ebid,
                    popularity=popularity)
            except Exception as e:
                logger.exception("[EBID:" + ebay_item.ebid + "] " + str(e))

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


if __name__ == "__main__":
    main(sys.argv[1:])

import sys, os

sys.path.append('%s/../../' % os.path.dirname(__file__))

import json

from ebaysdk.trading import Connection as Trading
from ebaysdk.exception import ConnectionError

from amazonmws import settings, utils
from amazonmws.models import StormStore, AmazonItem, AmazonItemPicture, Scraper, EbayItem, ItemQuantityHistory, Task
from amazonmws.errors import record_trade_api_error
from amazonmws.loggers import GrayLogger as logger, StaticFieldFilter, get_logger_name
from amazonmws.monitor.amazon_item import PriceMonitor


class EbayItemPolicyAppend(object):

    ebay_item = None
    quantity_updated = False

    TASK_ID = 888

    min_quantity = 5

    def __init__(self, ebay_item):
        self.ebay_item = ebay_item
        logger.addFilter(StaticFieldFilter(get_logger_name(), Task.get_name(self.TASK_ID)))

    def run(self):
        """ - check ebay quantity
        """

        self.__append_policy();
        return True


    def __append_policy(self):
        ret = False

        item_obj = {
            "Description": "<![CDATA[\n" + utils.get_policy_for_ebay_item_description() + "\n]]>",
            "ItemID": self.ebay_item.ebid
        }

        try:
            api = Trading(debug=True, warnings=True, domain=settings.EBAY_TRADING_API_DOMAIN, config_file=os.path.join(settings.CONFIG_PATH, 'ebay.yaml'))
            api.execute('AddToItemDescription', item_obj)

            if api.response.content:
                data = json.loads(api.response.json())

                # print json.dumps(data, indent=4, sort_keys=True)

                if ('ack' in data and data['ack'] == "Success") or ('Ack' in data and data['Ack'] == "Success"):
                    ret = True

                else:
                    logger.error(api.response.json())
                    record_trade_api_error(
                        item_obj['MessageID'], 
                        u'AddToItemDescription', 
                        utils.dict_to_json_string(item_obj),
                        api.response.json(),
                        amazon_item_id=self.ebay_item.amazon_item_id,
                        asin=self.ebay_item.asin,
                        ebay_item_id=self.ebay_item.id,
                        ebid=self.ebay_item.ebid
                    )

        except ConnectionError, e:
            logger.exception("[EBID:" + self.ebay_item.ebid + "] " + str(e))

        return ret


if __name__ == "__main__":
    
    active_ebay_items = StormStore.find(EbayItem, EbayItem.status == EbayItem.STATUS_ACTIVE)
    num_updated = 0

    if active_ebay_items.count() > 0:
        for ebay_item in active_ebay_items:
            monitor = EbayItemPolicyAppend(ebay_item)
            monitor.run()
            num_updated += 1

        logger.info("Number of ebay item policy appended: " + str(num_updated) + " items")


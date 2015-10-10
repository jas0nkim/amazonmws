import sys, os

sys.path.append('%s/../../' % os.path.dirname(__file__))

import datetime
import time
import uuid
import json

from storm.exceptions import StormError

from ebaysdk.trading import Connection as Trading
from ebaysdk.exception import ConnectionError

from amazonmws import settings
from amazonmws import utils
from amazonmws.models import StormStore, AmazonItem, AmazonItemPicture, Scraper, ScraperAmazonItem, EbayItem, EbayListingError, ItemPriceHistory, Task
from amazonmws.ebaystore.listing import calculate_profitable_price
from amazonmws.errors import record_trade_api_error
from amazonmws.loggers import GrayLogger as logger, StaticFieldFilter, get_logger_name
from amazonmws.monitor.amazon_item_monitor import AmazonItemMonitor


class UrgentPaypalAccountReviser(object):

    ebay_item = None
    amazon_item = None

    updated = False

    # since this is one time urgent task, there is no specifi task id
    # 
    # TASK_ID = Task.ebay_task_monitoring_quantity_changes

    def __init__(self, ebay_item):
        self.ebay_item = ebay_item
        self.amazon_item = self.__get_amazon_item()
        # logger.addFilter(StaticFieldFilter(get_logger_name(), Task.get_name(self.TASK_ID)))

    def __get_amazon_item(self):
        try:
            amazon_item = StormStore.find(AmazonItem, AmazonItem.id == self.ebay_item.amazon_item_id).one()
            if amazon_item:
                return amazon_item

            return None

        except StormError:
            return None

    def run(self):
        """ - check ebay quantity
        """

        logger.info("[EBID: " + self.ebay_item.ebid + "] " + "start updating paypal account...")

        ebay_item_url = settings.EBAY_ITEM_LINK_FORMAT % self.ebay_item.ebid

        result = self.__revise_paypal_account()

        if result:
            self.updated = True

        return True

    def __revise_paypal_account(self):
        ret = False
        ebay_price = calculate_profitable_price(self.amazon_item.price)

        if ebay_price < self.amazon_item.price:
            logger.error("[EBID:" + self.ebay_item.ebid  + "] " + "error on ebay price calculation (amazon price: $" + self.amazon_item.price + ", ebay price: $" + ebay_price + ")")
            return ret

        item_obj = {
            "MessageID": uuid.uuid4(),
            "Item": {
                "ItemID": self.ebay_item.ebid,
                "PrimaryCategory": {
                    "CategoryID": self.ebay_item.ebay_category_id,
                },
                "PayPalEmailAddress": settings.PAYPAL_ACCOUNT,
                "StartPrice": ebay_price,
            }
        }

        try:
            api = Trading(debug=True, warnings=True, domain=settings.EBAY_TRADING_API_DOMAIN)
            api.execute('ReviseFixedPriceItem', item_obj)

            if api.response.content:
                data = json.loads(api.response.json())

                # print json.dumps(data, indent=4, sort_keys=True)

                if ('ack' in data and data['ack'] == "Success") or ('Ack' in data and data['Ack'] == "Success"):
                    
                    ret = True
                    self.__record_history(ebay_price)

                else:
                    logger.error(api.response.json())
                    record_trade_api_error(
                        item_obj['MessageID'], 
                        u'ReviseFixedPriceItem', 
                        utils.dict_to_json_string(item_obj),
                        api.response.json(), 
                        amazon_item_id=self.amazon_item.id,
                        asin=self.amazon_item.asin,
                        ebay_item_id=self.ebay_item.id,
                        ebid=self.ebay_item.ebid
                    )

        except ConnectionError, e:
            logger.exception("[EBID:" + self.ebay_item.ebid  + "] " + str(e))

        return ret

    def __record_history(self, ebay_price):
        try:
            # update ebay_items table
            self.ebay_item.eb_price = ebay_price
            StormStore.add(self.ebay_item)
            
            # log into item_price_history table
            price_history = ItemPriceHistory()
            price_history.amazon_item_id = self.amazon_item.id
            price_history.asin = self.amazon_item.asin
            price_history.ebay_item_id = self.ebay_item.id
            price_history.ebid = self.ebay_item.ebid
            price_history.am_price = self.amazon_item.price
            price_history.eb_price = self.ebay_item.eb_price
            price_history.created_at = datetime.datetime.now()
            price_history.updated_at = datetime.datetime.now()                    
            StormStore.add(price_history)

            StormStore.commit()

            logger.info("[EBID: " + self.ebay_item.ebid + "] " + "PRICE UPDATED both amazon_item: $" + str(self.amazon_item.price) + ", and ebay_item: $" + str(self.ebay_item.eb_price))

        except StormError, e:
            logger.exception("[EBID: " + self.ebay_item.ebid + "] " + str(e))

if __name__ == "__main__":
    
    active_ebay_items = StormStore.find(EbayItem, EbayItem.status == EbayItem.STATUS_ACTIVE)
    num_updated = 0

    if active_ebay_items.count() > 0:
        for ebay_item in active_ebay_items:
            monitor = UrgentPaypalAccountReviser(ebay_item)
            monitor.run()

            if monitor.updated:
                logger.info("[EBID: " + ebay_item.ebid + "] " + "updated successfully")
                num_updated += 1
        
                break
        
        logger.info("Number of ebay item updated: " + str(num_updated) + " items")


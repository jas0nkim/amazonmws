import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

import datetime
import time
import uuid
import json

from storm.exceptions import StormError

from ebaysdk.trading import Connection as Trading
from ebaysdk.exception import ConnectionError

from amazonmws import settings
from amazonmws import utils
from amazonmws.models import StormStore, AmazonItem, AmazonItemPicture, Scraper, EbayItem, ItemPriceHistory, Task, EbayStore
from amazonmws.errors import record_trade_api_error
from amazonmws.loggers import GrayLogger as logger, StaticFieldFilter, get_logger_name


class UrgentReviser(object):
    ebay_store = None
    ebay_item = None
    amazon_item = None

    updated = False

    # since this is one time urgent task, there is no specifi task id
    # 
    TASK_ID = Task.ebay_task_revise_item

    def __init__(self, ebay_store, ebay_item):
        self.ebay_store = ebay_store
        self.ebay_item = ebay_item
        self.amazon_item = self.__get_amazon_item()
        logger.addFilter(StaticFieldFilter(get_logger_name(), Task.get_name(self.TASK_ID)))

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

        logger.info("[EBID: " + self.ebay_item.ebid + "] " + "start revising items...")

        ebay_item_url = settings.EBAY_ITEM_LINK_FORMAT % self.ebay_item.ebid

        ebay_price = utils.calculate_profitable_price(self.amazon_item.price, self.ebay_store)

        result = self.__revise_description(ebay_price)

        if result:
            self.__record_history(ebay_price)
            self.updated = True

        return True

    def __revise_fixed_price_item(self, item_obj):
        ret = False

        try:
            token = None if settings.APP_ENV == 'stage' else self.ebay_store.token
            api = Trading(debug=True, warnings=True, domain=settings.EBAY_TRADING_API_DOMAIN, token=token, config_file=os.path.join(settings.CONFIG_PATH, 'ebay.yaml'))
            api.execute('ReviseFixedPriceItem', item_obj)

            if api.response.content:
                data = json.loads(api.response.json())

                # print json.dumps(data, indent=4, sort_keys=True)

                if ('ack' in data and data['ack'] == "Success") or ('Ack' in data and data['Ack'] == "Success"):
                    
                    ret = True

                elif ('ack' in data and data['ack'] == "Warning") or ('Ack' in data and data['Ack'] == "Warning"):

                    if isinstance(data['Errors'], list):
                        error_code = data['Errors'][len(data['Errors']) - 1]['ErrorCode']
                        error_message = data['Errors'][len(data['Errors']) - 1]['LongMessage']
                    else:
                        error_code = data['Errors']['ErrorCode']
                        error_message = data['Errors']['LongMessage']

                    if error_code == "21919189" or error_code == 21919189 or error_code == "21917236" or error_code == 21917236:

                        logger.warning("[EBID:" + self.ebay_item.ebid  + "] " + error_message)
                        ret = True
                    else:
                        logger.warning(api.response.json())
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

        except ConnectionError as e:
            logger.exception("[EBID:" + self.ebay_item.ebid  + "] " + str(e))

        return ret

    def __revise_description(self, ebay_price):
        ret = False

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
                "Description": "<![CDATA[\n" + utils.apply_ebay_listing_template(self.amazon_item, self.ebay_store) + "\n]]>"
            }
        }
        return self.__revise_fixed_price_item(item_obj)

    def __revise_price_and_description(self, ebay_price):
        ret = False

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
                "StartPrice": ebay_price,
                "Quantity": settings.EBAY_ITEM_DEFAULT_QUANTITY,
                "Description": "<![CDATA[\n" + utils.apply_ebay_listing_template(self.amazon_item, self.ebay_store) + "\n]]>"
            }
        }
        return self.__revise_fixed_price_item(item_obj)

    def __revise_paypal_account(self, ebay_price):
        ret = False

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
                "PayPalEmailAddress": settings.STAGE_PAYPAL_ACCOUNT if settings.APP_ENV == 'stage' else self.ebay_store.paypal_username,
                "StartPrice": ebay_price,
                "Quantity": settings.EBAY_ITEM_DEFAULT_QUANTITY,
            }
        }
        return self.__revise_fixed_price_item(item_obj)

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

        except StormError as e:
            logger.exception("[EBID: " + self.ebay_item.ebid + "] " + str(e))


if __name__ == "__main__":

    try:
        ebay_store = StormStore.find(EbayStore, EbayStore.id == 3).one()
        
        if not ebay_store:
            logger.error('No ebay store found')
            raise Exception('No ebay store found')

    except StormError as e:
        logger.exception(e)
        raise e
    
    # ebay_items = StormStore.find(EbayItem, 
    #     EbayItem.ebay_store_id == ebay_store.id,
    #     EbayItem.status == EbayItem.STATUS_ACTIVE)

    ebay_items = StormStore.find(EbayItem, EbayItem.ebay_store_id == ebay_store.id)
    
    num_updated = 0

    if ebay_items.count() > 0:
        for ebay_item in ebay_items:
            monitor = UrgentReviser(ebay_store, ebay_item)
            monitor.run()

            if monitor.updated:
                logger.info("[EBID: " + ebay_item.ebid + "] " + "updated successfully")
                num_updated += 1
        
        logger.info("Number of ebay item updated: " + str(num_updated) + " items")


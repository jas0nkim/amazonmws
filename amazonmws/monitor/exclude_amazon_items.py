import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from storm.exceptions import StormError
from amazonmws.models import StormStore, AmazonItem, LookupAmazonItem, EbayItem, Task
from amazonmws.loggers import GrayLogger as logger, StaticFieldFilter, get_logger_name


def exclude_amazin_item(amazon_item):
    
    logger.addFilter(StaticFieldFilter(get_logger_name(), Task.get_name(Task.amazon_task_exclude_item)))

    try:
        amazon_item.status = AmazonItem.STATUS_EXCLUDED
        StormStore.add(amazon_item)
        StormStore.commit()
    except StormError, e:
        logger.exception("[ASIN: " + amazon_item.asin + "] " + "Failed to update status to STATUS_EXCLUDED")
        StormStore.rollback()
        return False
    
    ebay_item = get_ebay_item(amazon_item)
    if ebay_item != None:
        logger.debug("[EBID: " + ebay_item.ebid + "] " + "Updating status")
        try:
            ebay_item.status = EbayItem.STATUS_INACTIVE
            StormStore.add(ebay_item)
            StormStore.commit()
        except StormError, e:
            logger.exception("[EBID: " + ebay_item.ebid + "] " + "Failed to update status to STATUS_INACTIVE")
            StormStore.rollback()
            return False
    return True

def get_ebay_item(amazon_item):
    ebay_item = None
    try:
        ebay_item = StormStore.find(EbayItem,
            EbayItem.amazon_item_id == amazon_item.id,
            EbayItem.status != EbayItem.STATUS_INACTIVE).one()
    except StormError, e:
        logger.exception("[ASIN: " + amazon_item.asin + "] " + "Failed to fetch related INACTIVE ebay item")
    return ebay_item


if __name__ == "__main__":

    try:
        # exclude all amazon items with lookup id = 1, 2
        excluding_amazon_items = StormStore.find(AmazonItem,
            LookupAmazonItem.amazon_item_id == AmazonItem.id,
            (LookupAmazonItem.lookup_id == 1 or LookupAmazonItem.lookup_id == 2))
    except StormError, e:
        logger.exception("Failed to retrieve excluding amazon items")
        StormStore.rollback()
        raise e

    for amazon_item in excluding_amazon_items:
        exclude_amazin_item(amazon_item)



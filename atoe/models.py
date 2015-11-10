import datetime

from storm.expr import Select
from storm.exceptions import StormError

from amazonmws import settings as amazonmws_settings, utils as amazonmws_utils
from amazonmws.models import StormStore, zzAmazonItem as AmazonItem,
    zzAmazonItemPicture as AmazonItemPicture, zzAtoECategoryMap as AtoECategoryMap,
    EbayStore, EbayItem
from amazonmws.loggers import GrayLogger as logger


class EbayStoreModelManager(object):

    @staticmethod
    def fetch():
        return StormStore.find(EbayStore)


class EbayItemModelManager(object):

    @staticmethod
    def create(ebay_store, asin, ebid, category_id, eb_price):
        try:
            ebay_item = EbayItem()
            ebay_item.ebay_store_id = ebay_store.id
            ebay_item.asin = asin
            ebay_item.ebid = ebid
            ebay_item.ebay_category_id = category_id
            ebay_item.eb_price = eb_price
            ebay_item.quantity = amazonmws_settings.EBAY_ITEM_DEFAULT_QUANTITY
            ebay_item.status = EbayItem.STATUS_ACTIVE
            ebay_item.created_at = datetime.datetime.now()
            ebay_item.updated_at = datetime.datetime.now()
            StormStore.add(ebay_item)
            StormStore.commit()
            return True
        except StormError:
            StormStore.rollback()
            logger.exception("[%s|ASIN:%s|EBID:%s] Failed to store information in ebay_items table" % (ebay_store.username, asin, ebid))
            return False


class AmazonItemModelManager(object):

    @staticmethod
    def fetch_filtered():
        """filter amazon item by:
            - amazon active item
            - item which has not listed at ebay store
            - scraper (if applicable)

            return type: list
        """

        result = []
        try:
            filtered_items = StormStore.find(AmazonItem,
                LookupAmazonItem.amazon_item_id == AmazonItem.id,
                LookupOwnership.lookup_id == LookupAmazonItem.lookup_id,
                LookupOwnership.ebay_store_id == self.ebay_store.id,
                AmazonItem.status == AmazonItem.STATUS_ACTIVE,
                AmazonItem.review_count >= self.__min_review_count).order_by(Desc(AmazonItem.avg_rating), Desc(AmazonItem.review_count))
        except StormError:
            logger.exception('Unable to filter amazon items')

        # workaround solution - stupid but storm doesn't support outer join...
        # what it supposes to do - i.e.
        #   SELECT * FROM pets AS p 
        #       LEFT OUTER JOIN lost-pets AS lp
        #       ON p.name = lp.name
        #       WHERE lp.id IS NULL
        #       
        # ref: http://stackoverflow.com/a/369861
        num_items = 0

        for amazon_item in filtered_items:
            if isinstance(self.__asins_exclude, list) and len(self.__asins_exclude) > 0:
                if amazon_item.asin in self.__asins_exclude:
                    continue
            ebay_item = False
            try:
                ebay_item = StormStore.find(EbayItem, 
                    EbayItem.amazon_item_id == amazon_item.id,
                    EbayItem.ebay_store_id == self.ebay_store.id).one()
            
            except StormError:
                logger.exception("[ASIN:" + amazon_item.asin + "] " + "Error on finding item in ebay_items table")
                continue

            if not ebay_item:
                num_items += 1
                item_set = (amazon_item, None)
                result.append(item_set)
            
            elif ebay_item.status == EbayItem.STATUS_OUT_OF_STOCK:
                """add OOS ebay item - need to restock to ebay because it's been restocked on amazon!
                """
                num_items += 1
                item_set = (amazon_item, ebay_item)
                result.append(item_set)

        logger.info("[" + self.ebay_store.username + "] " + "Number of items to list on ebay: " + str(num_items) + " items")

        return result



class AtoECategoryMapModelManager(object):

    @staticmethod
    def fetch():
        return StormStore.find(AtoECategoryMap)

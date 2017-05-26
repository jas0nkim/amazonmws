import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'rfi'))

from django.db import connection
from django.core.exceptions import MultipleObjectsReturned

from amazonmws import settings, utils
from amazonmws.loggers import GrayLogger as logger

from rfi_orders.models import *


class EbayOrderModelManager(object):

    @staticmethod
    def create(ebay_store,
            order_id,
            record_number,
            total_price,
            shipping_cost=None,
            buyer_email=None,
            buyer_user_id=None,
            buyer_status=None,
            buyer_shipping_name=None,
            buyer_shipping_street1=None,
            buyer_shipping_street2=None,
            buyer_shipping_city_name=None,
            buyer_shipping_state_or_province=None,
            buyer_shipping_postal_code=None,
            buyer_shipping_country=None,
            buyer_shipping_phone=None,
            order_status=None,
            checkout_status=None,
            payment_status=None,
            creation_time=None,
            paid_time=None,
            feedback_left=False):
        
        kw = {
            'ebay_store_id': ebay_store.id,
            'order_id': order_id,
            'record_number': record_number,
            'total_price': total_price,
            'shipping_cost': shipping_cost,
            'buyer_email': buyer_email,
            'buyer_user_id': buyer_user_id,
            'buyer_status': buyer_status,
            'buyer_shipping_name': buyer_shipping_name,
            'buyer_shipping_street1': buyer_shipping_street1,
            'buyer_shipping_street2': buyer_shipping_street2,
            'buyer_shipping_city_name': buyer_shipping_city_name,
            'buyer_shipping_state_or_province': buyer_shipping_state_or_province,
            'buyer_shipping_postal_code': buyer_shipping_postal_code,
            'buyer_shipping_country': buyer_shipping_country,
            'buyer_shipping_phone': buyer_shipping_phone,
            'order_status': order_status,
            'checkout_status': checkout_status,
            'payment_status': payment_status,
            'creation_time': creation_time,
            'paid_time': paid_time,
            'feedback_left': feedback_left,
        }
        obj, created = EbayOrder.objects.update_or_create(**kw)
        return obj

    @staticmethod
    def fetch_one(**kw):
        if 'id' in kw:
            try:
                return EbayOrder.objects.get(id=kw['id'])
            except MultipleObjectsReturned as e:
                logger.error("[EbayOrderID:%s] Multiple order id exists in the system" % kw['id'])
                return None
            except EbayOrder.DoesNotExist as e:
                logger.warning("[EbayOrderID:%s] Order id not exists in the system" % kw['id'])
                return None
        elif 'order_id' in kw:
            try:
                return EbayOrder.objects.get(order_id=kw['order_id'])
            except MultipleObjectsReturned as e:
                logger.error("[EbayOrderID:%s] Multiple order id exists in the system" % kw['order_id'])
                return None
            except EbayOrder.DoesNotExist as e:
                logger.warning("[EbayOrderID:%s] Order id not exists in the system" % kw['order_id'])
                return None
        else:
            return None

    @staticmethod
    def fetch(order=None, desc=False, limit=None, **kw):
        ebay_orders = EbayOrder.objects.filter(**kw)
        if order:
            if desc == True:
                ebay_orders = ebay_orders.order_by('-{}'.format(order))
            else:
                ebay_orders = ebay_orders.order_by(order)
        if limit:
            ebay_orders = ebay_orders[:limit]
        return ebay_orders

    @staticmethod
    def update(order, **kw):
        if isinstance(order, EbayOrder):
            for key, value in kw.iteritems():
                setattr(order, key, value)
            order.save()
            return True
        return False

    @staticmethod
    def fetch_reports(ebay_store_id, durationtype='daily'):
        """ return: a set of sets:
                (orders,
                sales,
                ebay_fees,
                paypal_fees,
                amazon_costs,
                profits,
                profit_percentages,
                c_date)
        """
        ret = ()

        _groupby = 'DATE'
        if durationtype == 'weekly':
            _groupby = 'WEEK'
        elif durationtype == 'monthly':
            _groupby = 'MONTH'

        query = """SELECT
            COUNT(e.id) AS orders,
            SUM(e.total_price) AS sales,
            ROUND(SUM(e.total_price * 0.09), 2) AS ebay_fees,
            ROUND(SUM(e.total_price * 0.037 + 0.30), 2) AS paypal_fees,
            SUM(a.total) AS amazon_costs,
            ROUND(SUM(e.total_price - (e.total_price * 0.09) - (e.total_price * 0.037 + 0.30) - a.total), 2) AS profits,
            ROUND(SUM(e.total_price - (e.total_price * 0.09) - (e.total_price * 0.037 + 0.30) - a.total) / SUM(e.total_price) * 100, 1) AS profit_percentages,
            ROUND(SUM(e.total_price) / COUNT(e.id), 2) as average_sold_price,
            ROUND(SUM(e.total_price - (e.total_price * 0.09) - (e.total_price * 0.037 + 0.30) - a.total) / COUNT(e.id), 2) as average_profit,
            DATE(e.creation_time) AS c_date,
            SUM(eor.refunded_count) AS refunded_counts,
            SUM(eor.refunded_amount) AS refunded_amounts
        FROM ebay_orders e
            INNER JOIN ebay_order_amazon_orders eao ON eao.ebay_order_id = e.order_id
            INNER JOIN amazon_orders a ON eao.amazon_order_id = a.order_id
            INNER JOIN (select i.order_id, IF (r.act_refund_amount IS NULL, 0, 1) as refunded_count, IFNULL (SUM(r.act_refund_amount), 0) as refunded_amount from ebay_order_items as i left join ebay_order_returns as r on r.transaction_id = i.transaction_id group by i.order_id) eor on eor.order_id = e.order_id
        WHERE e.ebay_store_id = {ebay_store_id} AND e.order_status NOT IN ('Cancelled', 'CancelPending', 'Active') AND (e.payment_status IS NULL OR e.payment_status NOT IN ('Failed', 'Pending'))
        GROUP BY YEAR(e.creation_time), {group_by}(e.creation_time) ORDER BY c_date DESC""".format(
            ebay_store_id=ebay_store_id,
            group_by=_groupby)

        with connection.cursor() as cursor:
            cursor.execute(query);
            ret = cursor.fetchall()
        return ret

    @staticmethod
    def fetch_bestsellers(ebay_store_id, days=30):
        ret = ()
        query = """SELECT
            eoi.ebid,
            ai.asin,
            ai.title,
            ai.brand_name,
            ai.category,
            ei.created_at,
            COUNT(eoi.id) as total_solds,
            SUM(IF(eo.payment_status = 'Succeeded' AND eo.order_status <> 'Completed', 1, 0)) as total_cancels,
            SUM(IF(eor.id IS NULL, 0, 1)) as total_returns 
        FROM ebay_order_items eoi
            LEFT JOIN ebay_items ei ON ei.ebid = eoi.ebid
            LEFT JOIN amazon_items ai ON eoi.sku = ai.asin
            LEFT JOIN ebay_orders eo ON eo.order_id = eoi.order_id
            LEFT JOIN ebay_order_returns eor ON eor.transaction_id = eoi.transaction_id
        WHERE eo.ebay_store_id = {ebay_store_id} AND eo.creation_time BETWEEN CURDATE() - INTERVAL {days} DAY AND CURDATE()
        GROUP BY eoi.ebid ORDER BY total_solds DESC LIMIT 500""".format(
            ebay_store_id=ebay_store_id,
            days=days)

        with connection.cursor() as cursor:
            cursor.execute(query);
            ret = cursor.fetchall()
        return ret


class EbayOrderItemModelManager(object):
    
    @staticmethod
    def create(ebay_order,
            order_id,
            ebid,
            transaction_id,
            title=None,
            sku=None,
            quantity=None,
            price=None,
            is_variation=False):
        
        kw = {
            'ebay_order_id': ebay_order.id,
            'order_id': order_id,
            'ebid': ebid,
            'transaction_id': transaction_id,
            'title': title,
            'sku': sku,
            'quantity': quantity,
            'price': price,
            'is_variation': is_variation,
        }
        obj, created = EbayOrderItem.objects.update_or_create(**kw)
        return created

    @staticmethod
    def fetch(**kw):
        return EbayOrderItem.objects.filter(**kw)

    @staticmethod
    def fetch_one(**kw):
        if 'transaction_id' in kw:
            try:
                return EbayOrderItem.objects.get(transaction_id=kw['transaction_id'])
            except MultipleObjectsReturned as e:
                logger.error("[EbayOrderTransID:{}] Multiple ebay order items exist in the system" % kw['transaction_id'])
                return None
            except EbayOrderItem.DoesNotExist as e:
                return None
        else:
            return None

class AmazonOrderModelManager(object):

    @staticmethod
    def create(
            order_id,
            amazon_account_id,
            item_price,
            shipping_and_handling,
            tax,
            total,
            buyer_shipping_name=None,
            buyer_shipping_street1=None,
            buyer_shipping_street2=None,
            buyer_shipping_city_name=None,
            buyer_shipping_state_or_province=None,
            buyer_shipping_postal_code=None,
            buyer_shipping_country=None,
            buyer_shipping_phone=None,
            carrier=None,
            tracking_number=None):

        kw = {
            'order_id': order_id,
            'amazon_account_id': amazon_account_id,
            'item_price': item_price,
            'shipping_and_handling': shipping_and_handling,
            'tax': tax,
            'total': total,
            'buyer_shipping_name': buyer_shipping_name,
            'buyer_shipping_street1': buyer_shipping_street1,
            'buyer_shipping_street2': buyer_shipping_street2,
            'buyer_shipping_city_name': buyer_shipping_city_name,
            'buyer_shipping_state_or_province': buyer_shipping_state_or_province,
            'buyer_shipping_postal_code': buyer_shipping_postal_code,
            'buyer_shipping_country': buyer_shipping_country,
            'buyer_shipping_phone': buyer_shipping_phone,
            'carrier': carrier,
            'tracking_number': tracking_number,
        }
        obj, created = AmazonOrder.objects.update_or_create(**kw)
        return obj

    @staticmethod
    def update(amazon_order, **kw):
        if isinstance(amazon_order, AmazonOrder):
            for key, value in kw.iteritems():
                setattr(amazon_order, key, value)
            amazon_order.save()
            return True
        return False

    @staticmethod
    def fetch(**kw):
        return AmazonOrder.objects.filter(**kw)


class AmazonOrderItemModelManager(object):

    @staticmethod
    def create(amazon_order,
            order_id,
            asin,
            is_variation=False):

        kw = {
            'amazon_order_id': amazon_order.id,
            'order_id': order_id,
            'asin': asin,
            'is_variation': is_variation,
        }
        obj, created = AmazonOrderItem.objects.update_or_create(**kw)
        return obj


class EbayOrderAmazonOrderModelManager(object):

    @staticmethod
    def create(amazon_order_id, ebay_order_id):
        kw = {
            'amazon_order_id': amazon_order_id,
            'ebay_order_id': ebay_order_id,
        }
        obj, created = EbayOrderAmazonOrder.objects.update_or_create(**kw)
        return obj

    @staticmethod
    def fetch_one(**kw):
        if 'ebay_order_id' in kw:
            try:
                return EbayOrderAmazonOrder.objects.get(ebay_order_id=kw['ebay_order_id'])
            except MultipleObjectsReturned as e:
                logger.error("[EbayOrderID:%s] Multiple amazon orders exist in the system" % kw['ebay_order_id'])
                return None
            except EbayOrderAmazonOrder.DoesNotExist as e:
                return None
        elif 'amazon_order_id' in kw:
            try:
                return EbayOrderAmazonOrder.objects.get(amazon_order_id=kw['amazon_order_id'])
            except MultipleObjectsReturned as e:
                logger.error("[AmazonOrderID:%s] Multiple ebay orders exist in the system" % kw['amazon_order_id'])
                return None
            except EbayOrderAmazonOrder.DoesNotExist as e:
                return None
        else:
            return None

    @staticmethod
    def fetch(**kw):
        return EbayOrderAmazonOrder.objects.filter(**kw)


class EbayOrderShippingModelManager(object):

    @staticmethod
    def create(order_id, carrier, tracking_number, ebay_order=None):
        if ebay_order is None:
            ebay_order = EbayOrderModelManager.fetch_one(order_id=order_id)
        kw = {
            'ebay_order_id': ebay_order.id,
            'order_id': order_id,
            'carrier': carrier,
            'tracking_number': tracking_number,
        }
        obj, created = EbayOrderShipping.objects.update_or_create(**kw)
        return obj

    @staticmethod
    def fetch_one(**kw):
        if 'ebay_order_id' in kw:
            try:
                return EbayOrderShipping.objects.get(order_id=kw['ebay_order_id'])
            except MultipleObjectsReturned as e:
                logger.error("[EbayOrderID:%s] Multiple ebay order shipping exist in the system" % kw['ebay_order_id'])
                return None
            except EbayOrderShipping.DoesNotExist as e:
                return None
        elif 'carrier' in kw and 'tracking_number' in kw:
            try:
                return EbayOrderShipping.objects.get(carrier=kw['carrier'], tracking_number=kw['tracking_number'])
            except MultipleObjectsReturned as e:
                logger.error("[TrackingNumber:%s] Multiple ebay order shipping exist in the system" % kw['tracking_number'])
                return None
            except EbayOrderShipping.DoesNotExist as e:
                return None
        else:
            return None


class EbayOrderReturnModelManager(object):

    @staticmethod
    def create(**kw):
        obj = None
        try:
            obj = EbayOrderReturn(**kw)
            obj.save()
        except Exception as e:
            logger.error(str(e))
            return None
        return obj

    @staticmethod
    def update(order_return, **kw):
        if isinstance(order_return, EbayOrderReturn):
            for key, value in kw.iteritems():
                setattr(order_return, key, value)
            order_return.save()
            return True
        return False

    @staticmethod
    def fetch_one(**kw):
        if 'return_id' in kw:
            try:
                return EbayOrderReturn.objects.get(return_id=kw['return_id'])
            except MultipleObjectsReturned as e:
                logger.error("[EBAYRETURNID:{}] Multile ebay order returns exist".format(kw['return_id']))
                return None
            except EbayOrderReturn.DoesNotExist as e:
                logger.warning("[EBAYRETURNID:{}] No ebay order return found".format(kw['return_id']))
                return None
        else:
            return None

    @staticmethod
    def fetch(order='return_id', desc=True, limit=None, **kw):
        ebay_order_returns = EbayOrderReturn.objects.filter(**kw)
        if order:
            if desc == True:
                ebay_order_returns = ebay_order_returns.order_by('-{}'.format(order))
            else:
                ebay_order_returns = ebay_order_returns.order_by(order)
        if limit:
            ebay_order_returns = ebay_order_returns[:limit]
        return ebay_order_returns


class AmazonOrderReturnModelManager(object):

    @staticmethod
    def create(**kw):
        obj = None
        try:
            obj = AmazonOrderReturn(**kw)
            obj.save()
        except Exception as e:
            logger.error(str(e))
            return None
        return obj

    @staticmethod
    def update(order_return, **kw):
        if isinstance(order_return, AmazonOrderReturn):
            for key, value in kw.iteritems():
                setattr(order_return, key, value)
            order_return.save()
            return True
        return False

    @staticmethod
    def fetch_one(**kw):
        if 'order_id' in kw and 'asin' in kw:
            try:
                return AmazonOrderReturn.objects.get(order_id=kw['order_id'], asin=kw['asin'])
            except MultipleObjectsReturned as e:
                logger.error("[AMAZONORDID:{}|ASIN:{}] Multile amazon order returns exist".format(kw['return_id'], kw['asin']))
                return None
            except AmazonOrderReturn.DoesNotExist as e:
                logger.warning("[AMAZONORDID:{}|ASIN:{}] No amazon order return found".format(kw['return_id'], kw['asin']))
                return None
        if 'ebay_return_id' in kw:
            try:
                return AmazonOrderReturn.objects.get(ebay_return_id=kw['ebay_return_id'])
            except MultipleObjectsReturned as e:
                logger.error("[EBAYORDID:{}] Multile amazon order returns exist".format(kw['ebay_return_id']))
                return None
            except AmazonOrderReturn.DoesNotExist as e:
                logger.warning("[EBAYORDID:{}] No amazon order return found".format(kw['ebay_return_id']))
                return None
        else:
            return None

    @staticmethod
    def fetch(order='created_at', desc=True, limit=None, **kw):
        amazon_order_returns = AmazonOrderReturn.objects.filter(**kw)
        if order:
            if desc == True:
                amazon_order_returns = amazon_order_returns.order_by('-{}'.format(order))
            else:
                amazon_order_returns = amazon_order_returns.order_by(order)
        if limit:
            amazon_order_returns = amazon_order_returns[:limit]
        return amazon_order_returns

from __future__ import unicode_literals

from django.db import models
from rfi_account_profiles.models import EbayStore, AmazonAccount
from rfi_sources.models import AmazonItem
from rfi.fields import RfiForeignKey


class Transaction(models.Model):
    ebay_store = RfiForeignKey(EbayStore, on_delete=models.deletion.DO_NOTHING, blank=True, null=True, db_index=True)
    seller_user_id = models.CharField(max_length=100, db_index=True)
    transaction_id = models.CharField(max_length=100, db_index=True)
    item_id = models.CharField(max_length=100, db_index=True)
    order_id = models.CharField(max_length=100, db_index=True)
    external_transaction_id = models.CharField(max_length=100, blank=True, null=True, db_index=True)
    transaction_price = models.DecimalField(max_digits=15, decimal_places=2)
    sales_tax_percent = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    sales_tax_state = models.CharField(max_length=32, blank=True, null=True)
    sales_tax_amount = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    amount_paid = models.DecimalField(max_digits=15, decimal_places=2)
    buyer_email = models.CharField(max_length=100, blank=True, null=True)
    buyer_user_id = models.CharField(max_length=100, db_index=True)
    buyer_status = models.CharField(max_length=32)
    buyer_shipping_name = models.CharField(max_length=100)
    buyer_shipping_street1 = models.CharField(max_length=100, blank=True, null=True)
    buyer_shipping_street2 = models.CharField(max_length=100, blank=True, null=True)
    buyer_shipping_city_name = models.CharField(max_length=100, blank=True, null=True)
    buyer_shipping_state_or_province = models.CharField(max_length=100, blank=True, null=True)
    buyer_shipping_country = models.CharField(max_length=32, blank=True, null=True)
    buyer_shipping_country_name = models.CharField(max_length=100, blank=True, null=True)
    buyer_shipping_phone = models.CharField(max_length=100, blank=True, null=True)
    buyer_shipping_postal_code = models.CharField(max_length=100, blank=True, null=True)
    order_status = models.CharField(max_length=32)
    ebay_payment_status = models.CharField(max_length=32, blank=True, null=True)
    checkout_status = models.CharField(max_length=32, blank=True, null=True)
    complete_status = models.CharField(max_length=32, blank=True, null=True)
    payment_hold_status = models.CharField(max_length=32, blank=True, null=True)
    external_transaction_status = models.CharField(max_length=32, blank=True, null=True)
    carrier = models.CharField(max_length=100, blank=True, null=True)
    tracking_number = models.CharField(max_length=100, blank=True, null=True)
    raw_item = models.TextField(blank=True, null=True)
    raw_transactionarray = models.TextField(blank=True, null=True)
    raw_xml = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ts = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'transactions'


class AmazonOrder(models.Model):
    order_id = models.CharField(max_length=100, db_index=True, unique=True)
    amazon_account = RfiForeignKey(AmazonAccount, on_delete=models.deletion.DO_NOTHING, db_index=True)
    item_price = models.DecimalField(max_digits=15, decimal_places=2)
    shipping_and_handling = models.DecimalField(max_digits=15, decimal_places=2)
    savings = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    tax = models.DecimalField(max_digits=15, decimal_places=2)
    total = models.DecimalField(max_digits=15, decimal_places=2)
    buyer_shipping_name = models.CharField(max_length=100, blank=True, null=True)
    buyer_shipping_street1 = models.CharField(max_length=100, blank=True, null=True)
    buyer_shipping_street2 = models.CharField(max_length=100, blank=True, null=True)
    buyer_shipping_city_name = models.CharField(max_length=100, blank=True, null=True)
    buyer_shipping_state_or_province = models.CharField(max_length=100, blank=True, null=True)
    buyer_shipping_country = models.CharField(max_length=100, blank=True, null=True)
    buyer_shipping_phone = models.CharField(max_length=100, blank=True, null=True)
    buyer_shipping_postal_code = models.CharField(max_length=100, blank=True, null=True)
    carrier = models.CharField(max_length=100, blank=True, null=True)
    tracking_number = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ts = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}'.format(self.order_id)

    class Meta:
        db_table = 'amazon_orders'


class AmazonOrderItem(models.Model):
    amazon_order = RfiForeignKey('AmazonOrder', on_delete=models.deletion.DO_NOTHING, blank=True, null=True, db_index=True, related_name='ordered_items')
    order_id = models.CharField(max_length=100, db_index=True)
    asin = models.CharField(max_length=32, db_index=True, blank=True, null=True)
    is_variation = models.BooleanField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ts = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'amazon_order_items'


# class TransactionAmazonOrder(models.Model):
#     transaction = RfiForeignKey('Transaction', on_delete=models.deletion.DO_NOTHING, blank=True, null=True, db_index=True)
#     amazon_order = RfiForeignKey('AmazonOrder', on_delete=models.deletion.DO_NOTHING, blank=True, null=True, db_index=True)
#     internal_error_type = models.SmallIntegerField(blank=True, null=True)
#     internal_error_message = models.CharField(max_length=255, blank=True, null=True)
#     is_ordering_in_process = models.IntegerField(blank=True, null=True, default=0)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     ts = models.DateTimeField(auto_now=True)

#     class Meta:
#         db_table = 'transaction_amazon_orders'

class EbayOrder(models.Model):
    ebay_store = RfiForeignKey(EbayStore, on_delete=models.deletion.DO_NOTHING, blank=True, null=True, db_index=True)
    order_id = models.CharField(max_length=100, db_index=True, unique=True)
    record_number = models.IntegerField(default=0)
    total_price = models.DecimalField(max_digits=15, decimal_places=2)
    shipping_cost = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    buyer_email = models.CharField(max_length=100, db_index=True)
    buyer_user_id = models.CharField(max_length=100, db_index=True)
    buyer_status = models.CharField(max_length=32, blank=True, null=True)
    buyer_shipping_name = models.CharField(max_length=100, blank=True, null=True)
    buyer_shipping_street1 = models.CharField(max_length=100, blank=True, null=True)
    buyer_shipping_street2 = models.CharField(max_length=100, blank=True, null=True)
    buyer_shipping_city_name = models.CharField(max_length=100, blank=True, null=True)
    buyer_shipping_state_or_province = models.CharField(max_length=100, blank=True, null=True)
    buyer_shipping_postal_code = models.CharField(max_length=100, blank=True, null=True)
    buyer_shipping_country = models.CharField(max_length=32, blank=True, null=True)
    buyer_shipping_phone = models.CharField(max_length=100, blank=True, null=True)
    order_status = models.CharField(max_length=32, blank=True, null=True)
    payment_status = models.CharField(max_length=32, blank=True, null=True)
    checkout_status = models.CharField(max_length=32)
    creation_time = models.DateTimeField(blank=True, null=True, verbose_name="Placed at")
    paid_time = models.DateTimeField(blank=True, null=True)
    feedback_left = models.BooleanField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ts = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} | {}'.format(self.record_number, self.order_id)

    class Meta:
        db_table = 'ebay_orders'


class EbayOrderItem(models.Model):
    ebay_order = RfiForeignKey('EbayOrder', on_delete=models.deletion.DO_NOTHING, blank=True, null=True, db_index=True, related_name='ordered_items')
    order_id = models.CharField(max_length=100, db_index=True)
    ebid = models.CharField(max_length=100, db_index=True)
    transaction_id = models.CharField(max_length=100, db_index=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    sku = models.CharField(max_length=100, blank=True, null=True)
    quantity = models.SmallIntegerField(blank=True, null=True)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    is_variation = models.BooleanField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ts = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ebay_order_items'


class EbayOrderShipping(models.Model):
    ebay_order = RfiForeignKey('EbayOrder', on_delete=models.deletion.DO_NOTHING, blank=True, null=True, db_index=True, related_name='shipping')
    order_id = models.CharField(max_length=100, db_index=True)
    carrier = models.CharField(max_length=100, blank=True, null=True)
    tracking_number = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ts = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ebay_order_shippings'


class EbayOrderAmazonOrder(models.Model):
    ebay_order = RfiForeignKey('EbayOrder', on_delete=models.deletion.DO_NOTHING, blank=True, null=True, to_field="order_id", db_column="ebay_order_id", db_index=True)
    amazon_order = RfiForeignKey('AmazonOrder', on_delete=models.deletion.DO_NOTHING, blank=True, null=True, to_field="order_id", db_column="amazon_order_id", db_index=True)

    class Meta:
        db_table = 'ebay_order_amazon_orders'


class EbayOrderReturn(models.Model):
    # EbayOrderReturn.status values
    ebay_store = RfiForeignKey(EbayStore, on_delete=models.deletion.DO_NOTHING, blank=True, null=True, db_index=True)
    return_id = models.CharField(max_length=100, db_index=True)
    transaction_id = models.CharField(max_length=100, db_index=True)
    item_id = models.CharField(max_length=100, db_index=True)
    quantity = models.SmallIntegerField(blank=True, null=True)
    buyer_username = models.CharField(max_length=100, db_index=True)
    est_refund_amount = models.DecimalField(max_digits=15, decimal_places=2)
    act_refund_amount = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    reason = models.CharField(max_length=100, blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    carrier = models.CharField(max_length=100, blank=True, null=True)
    tracking_number = models.CharField(max_length=100, blank=True, null=True)
    rma = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    creation_time = models.DateTimeField(blank=True, null=True)
    raw_data = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ts = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ebay_order_returns'


class AmazonOrderReturn(models.Model):
    # AmazonOrderReturn.status values
    STATUS_INITIATED = 'INITIATED'
    STATUS_SHIPPING_LABEL_ISSUED = 'SHIPPING_LABEL_ISSUED'
    STATUS_RETURNED = 'RETURNED'
    STATUS_REFUNDED = 'REFUNDED'
    STATUS_CLOSED_WO_REFUND = 'CLOSED_WO_REFUND'
    STATUS_CANCELED = 'CANCELED'

    amazon_account = RfiForeignKey(AmazonAccount, on_delete=models.deletion.DO_NOTHING, db_index=True)
    order_id = models.CharField(max_length=100, db_index=True)
    asin = models.CharField(max_length=32, db_index=True, blank=True, null=True)
    return_id = models.CharField(max_length=100, db_index=True, blank=True, null=True)
    ebay_return_id = models.CharField(max_length=100, db_index=True, blank=True, null=True)
    quantity = models.SmallIntegerField(blank=True, null=True)
    refunded_amount = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    carrier = models.CharField(max_length=100, blank=True, null=True)
    tracking_number = models.CharField(max_length=100, blank=True, null=True)
    rma = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True)
    returned_date = models.DateField(blank=True, null=True)
    refunded_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ts = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'amazon_order_returns'


class EbayOrderAutomationError(models.Model):
    ebay_order = RfiForeignKey('EbayOrder', on_delete=models.deletion.DO_NOTHING, blank=True, null=True, to_field="order_id", db_column="ebay_order_id", db_index=True)
    error_message = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'ebay_order_automation_errors'

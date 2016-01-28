from __future__ import unicode_literals

from django.db import models
from rfi_account_profiles.models import EbayStore, AmazonAccount
from rfi_listings.models import EbayItem
from rfi_sources.models import AmazonItem


class Transaction(models.Model):
    ebay_store_id = models.IntegerField()
    seller_user_id = models.ForeignKey(EbayStore, on_delete=models.deletion.DO_NOTHING, to_field="username")
    transaction_id = models.CharField(max_length=100)
    item_id = models.ForeignKey(EbayItem, on_delete=models.deletion.DO_NOTHING, to_field="ebid")
    order_id = models.CharField(max_length=100)
    external_transaction_id = models.CharField(max_length=100, blank=True, null=True)
    transaction_price = models.DecimalField(max_digits=15, decimal_places=2)
    sales_tax_percent = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    sales_tax_state = models.CharField(max_length=32, blank=True, null=True)
    sales_tax_amount = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    amount_paid = models.DecimalField(max_digits=15, decimal_places=2)
    buyer_email = models.CharField(max_length=100, blank=True, null=True)
    buyer_user_id = models.CharField(max_length=100)
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

    class Meta:
        db_table = 'transactions'


class AmazonOrder(models.Model):
    order_id = models.CharField(max_length=100)
    asin = models.ForeignKey(AmazonItem, on_delete=models.deletion.DO_NOTHING, to_field="asin")
    amazon_account_id = models.ForeignKey(AmazonAccount, on_delete=models.deletion.DO_NOTHING)
    item_price = models.DecimalField(max_digits=15, decimal_places=2)
    shipping_and_handling = models.DecimalField(max_digits=15, decimal_places=2)
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

    class Meta:
        db_table = 'amazon_orders'


class TransactionAmazonOrder(models.Model):
    transaction_id = models.ForeignKey('Transaction', on_delete=models.deletion.DO_NOTHING)
    amazon_order_id = models.ForeignKey('AmazonOrder', on_delete=models.deletion.DO_NOTHING, blank=True, null=True)
    internal_error_type = models.SmallIntegerField(blank=True, null=True)
    internal_error_message = models.CharField(max_length=255, blank=True, null=True)
    is_ordering_in_process = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'transaction_amazon_orders'

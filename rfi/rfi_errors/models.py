from __future__ import unicode_literals

from django.db import models

from rfi_account_profiles.models import EbayStore
from rfi_sources.models import AmazonItem, EbayItemCategory
from rfi_listings.models import EbayItem


class EbayTradingApiError(models.Model):
    message_id = models.CharField(max_length=100)
    trading_api = models.CharField(max_length=100)
    request = models.TextField()
    response = models.TextField()
    error_code = models.IntegerField(blank=True, null=True, default=0)
    description = models.TextField(blank=True, null=True)
    amazon_item = models.ForeignKey(AmazonItem, blank=True, null=True, on_delete=models.CASCADE, to_field="asin", db_column="asin")
    ebay_item = models.ForeignKey(EbayItem, blank=True, null=True, on_delete=models.CASCADE, to_field="ebid", db_column="ebid")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ts = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ebay_trading_api_errors'


class EbayNotificationError(models.Model):
    correlation_id = models.CharField(max_length=100)
    event_name = models.CharField(max_length=100, blank=True, null=True)
    recipient_user_id = models.CharField(max_length=100, blank=True, null=True)
    ebay_store = models.ForeignKey(EbayStore, blank=True, null=True, on_delete=models.CASCADE)
    response = models.TextField()
    error_code = models.IntegerField(blank=True, null=True, default=0)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ts = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ebay_notification_errors'


class ErrorEbayInvalidCategory(models.Model):
    message_id = models.CharField(max_length=100)
    amazon_item = models.ForeignKey(AmazonItem, on_delete=models.CASCADE, to_field="asin", db_column="asin")
    amazon_category = models.CharField(max_length=255)
    ebay_category = models.ForeignKey(EbayItemCategory, blank=True, null=True, on_delete=models.deletion.DO_NOTHING, to_field="category_id")
    request = models.TextField()
    status = models.SmallIntegerField(blank=True, null=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ts = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'error_ebay_invalid_category'

from __future__ import unicode_literals

from django.db import models

from rfi_account_profiles.models import EbayStore
from rfi_sources.models import AmazonItem
from rfi_listings.models import EbayItem
from rfi.fields import RfiForeignKey


class EbayTradingApiError(models.Model):
    message_id = models.CharField(max_length=100, db_index=True)
    trading_api = models.CharField(max_length=100, db_index=True)
    request = models.TextField()
    response = models.TextField()
    error_code = models.IntegerField(blank=True, null=True, default=0)
    description = models.TextField(blank=True, null=True)
    asin = models.CharField(max_length=32, blank=True, null=True, db_index=True)
    ebid = models.CharField(max_length=100, blank=True, null=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ts = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ebay_trading_api_errors'


class EbayNotificationError(models.Model):
    correlation_id = models.CharField(max_length=100, db_index=True)
    event_name = models.CharField(max_length=100, blank=True, null=True)
    recipient_user_id = models.CharField(max_length=100, blank=True, null=True, db_index=True)
    ebay_store = RfiForeignKey(EbayStore, blank=True, null=True, on_delete=models.CASCADE, db_index=True)
    response = models.TextField()
    error_code = models.IntegerField(blank=True, null=True, default=0)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ts = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ebay_notification_errors'


class ErrorEbayInvalidCategory(models.Model):
    message_id = models.CharField(max_length=100, db_index=True)
    asin = models.CharField(max_length=32, blank=True, null=True, db_index=True)
    amazon_category = models.CharField(max_length=255, db_index=True)
    ebay_category_id = models.CharField(max_length=100, blank=True, null=True, db_index=True)
    request = models.TextField()
    status = models.SmallIntegerField(blank=True, null=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ts = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'error_ebay_invalid_category'

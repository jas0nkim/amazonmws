from __future__ import unicode_literals

from django.db import models


class EbayTradingApiError(models.Model):
    message_id = models.CharField(max_length=100)
    trading_api = models.CharField(max_length=100)
    request = models.TextField()
    response = models.TextField()
    error_code = models.IntegerField(blank=True, null=True, default=0)
    description = models.TextField(blank=True, null=True)
    amazon_item_id = models.IntegerField(blank=True, null=True, default=0)
    asin = models.CharField(max_length=32, blank=True, null=True)
    ebay_item_id = models.IntegerField(blank=True, null=True, default=0)
    ebid = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ts = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ebay_trading_api_errors'


class EbayNotificationError(models.Model):
    correlation_id = models.CharField(max_length=100)
    event_name = models.CharField(max_length=100, blank=True, null=True)
    recipient_user_id = models.CharField(max_length=100, blank=True, null=True)
    ebay_store_id = models.IntegerField(blank=True, null=True)
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
    asin = models.CharField(max_length=32)
    amazon_category = models.CharField(max_length=255)
    ebay_category = models.ForeignKey(EbayItemCategory, on_delete=models.deletion.DO_NOTHING, to_field="category_id", blank=True, null=True)
    request = models.TextField()
    status = models.SmallIntegerField(blank=True, null=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ts = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'error_ebay_invalid_category'

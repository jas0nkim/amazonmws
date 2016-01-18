from __future__ import unicode_literals

from django.db import models


class ItemPriceHistory(models.Model):
    amazon_item_id = models.IntegerField()
    asin = models.CharField(max_length=32)
    ebay_item_id = models.IntegerField(blank=True, null=True)
    ebid = models.CharField(max_length=100, blank=True, null=True)
    am_price = models.DecimalField(max_digits=15, decimal_places=2)
    eb_price = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'item_price_history'


class ItemStatusHistory(models.Model):
    amazon_item_id = models.IntegerField()
    asin = models.CharField(max_length=32)
    ebay_item_id = models.IntegerField(blank=True, null=True)
    ebid = models.CharField(max_length=100, blank=True, null=True)
    am_status = models.SmallIntegerField(blank=True, null=True)
    eb_status = models.SmallIntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'item_status_history'


class ItemQuantityHistory(models.Model):
    amazon_item_id = models.IntegerField()
    asin = models.CharField(max_length=32)
    ebay_item_id = models.IntegerField(blank=True, null=True)
    ebid = models.CharField(max_length=100, blank=True, null=True)
    quantity = models.SmallIntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'item_quantity_history'


class AmazonBestsellersArchived(models.Model):
    bestseller_category = models.CharField(max_length=255)
    bestseller_category_url = models.TextField()
    rank = models.SmallIntegerField()
    asin = models.CharField(max_length=32, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'zz__amazon_bestsellers_archived'

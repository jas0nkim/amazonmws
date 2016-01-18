from __future__ import unicode_literals

from django.db import models


class EbayItem(models.Model):
    ebay_store_id = models.IntegerField()
    asin = models.CharField(max_length=32)
    ebid = models.CharField(max_length=100)
    ebay_category_id = models.CharField(max_length=32)
    eb_price = models.DecimalField(max_digits=15, decimal_places=2)
    quantity = models.SmallIntegerField(blank=True, null=True)
    status = models.SmallIntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'ebay_items'


class ZzExclBrand(models.Model):
    brand_name = models.CharField(max_length=100)
    category = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'zz__excl_brands'


class ZzEbayStorePreferredCategory(models.Model):
    ebay_store_id = models.IntegerField()
    category_type = models.CharField(max_length=17)
    category_name = models.CharField(max_length=255)
    max_items = models.IntegerField(blank=True, null=True)
    priority = models.SmallIntegerField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'zz__ebay_store_preferred_categories'

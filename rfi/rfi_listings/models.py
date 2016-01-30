from __future__ import unicode_literals

from django.db import models
from rfi_sources.models import AmazonItem
from rfi_account_profiles.models import EbayStore

class EbayItem(models.Model):
    # EbayItem.status values
    STATUS_INACTIVE = 0 # ended item
    STATUS_ACTIVE = 1 # active item
    STATUS_OUT_OF_STOCK = 2

    ebay_store = models.ForeignKey(EbayStore, on_delete=models.CASCADE)
    amazon_item = models.ForeignKey(AmazonItem, on_delete=models.deletion.DO_NOTHING, to_field="asin")
    ebid = models.CharField(max_length=100, unique=True)
    ebay_item_category = models.ForeignKey(EbayItemCategory, on_delete=models.deletion.DO_NOTHING, to_field="category_id")
    eb_price = models.DecimalField(max_digits=15, decimal_places=2)
    quantity = models.SmallIntegerField(blank=True, null=True)
    status = models.SmallIntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ebay_items'


class ExclBrand(models.Model):
    brand_name = models.CharField(max_length=100)
    category = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'excl_brands'


class EbayStorePreferredCategory(models.Model):
    STATUS_ACTIVE = 1
    STATUS_INACTIVE = 0

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
        db_table = 'ebay_store_preferred_categories'

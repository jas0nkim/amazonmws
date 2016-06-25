from __future__ import unicode_literals

from django.db import models
from rfi_sources.models import AmazonItem, EbayItemCategory
from rfi_account_profiles.models import EbayStore
from rfi.fields import RfiForeignKey


class EbayItem(models.Model):
    # EbayItem.status values
    STATUS_INACTIVE = 0 # ended item
    STATUS_ACTIVE = 1 # active item
    STATUS_OUT_OF_STOCK = 2 # out of stock item

    ebay_store = RfiForeignKey(EbayStore, on_delete=models.CASCADE, db_index=True)
    amazon_item = RfiForeignKey(AmazonItem, on_delete=models.deletion.DO_NOTHING, to_field="asin", db_column="asin", db_index=True)
    ebid = models.CharField(max_length=100, unique=True, db_index=True)
    ebay_category_id = models.CharField(max_length=100, null=True, blank=True, db_index=True)
    eb_price = models.DecimalField(max_digits=15, decimal_places=2)
    quantity = models.SmallIntegerField(blank=True, null=True, default=0)
    status = models.SmallIntegerField(blank=True, null=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ts = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ebay_items'


class EbayItemStat(models.Model):
    ebid = models.CharField(max_length=100, unique=True, db_index=True)
    clicks = models.IntegerField(blank=True, null=True, default=0)
    watches = models.IntegerField(blank=True, null=True, default=0)
    solds = models.IntegerField(blank=True, null=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ts = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ebay_item_stats'


class ExclBrand(models.Model):
    brand_name = models.CharField(max_length=100, db_index=True)
    category = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ts = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'excl_brands'


class EbayStorePreferredCategory(models.Model):
    CATEGORY_TYPE_AMAZON = 'amazon'
    CATEGORY_TYPE_AMAZON_BESTSELLER = 'amazon_bestseller'
    CATEGORY_TYPE_CHOICES = (
        (CATEGORY_TYPE_AMAZON, 'amazon'),
        (CATEGORY_TYPE_AMAZON_BESTSELLER, 'amazon_bestseller'),
    )

    STATUS_ACTIVE = 1
    STATUS_INACTIVE = 0

    ebay_store = RfiForeignKey(EbayStore, on_delete=models.CASCADE, db_index=True)
    category_type = models.CharField(max_length=17, choices=CATEGORY_TYPE_CHOICES, default=CATEGORY_TYPE_AMAZON)
    category_name = models.CharField(max_length=255)
    category_url = models.TextField(default='')
    max_items = models.IntegerField(blank=True, null=True, default=0)
    priority = models.SmallIntegerField(blank=True, null=True, default=0)
    status = models.SmallIntegerField(blank=True, null=True, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ts = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '[ebaystore:{}] {} - {}'.format(self.ebay_store.username, self.category_type, self.category_name)

    class Meta:
        db_table = 'ebay_store_preferred_categories'

class AmazonScrapeTask(models.Model):
    task_id = models.CharField(max_length=255, db_index=True)
    ebay_store = RfiForeignKey(EbayStore, on_delete=models.CASCADE, db_index=True)
    amazon_item = RfiForeignKey(AmazonItem, on_delete=models.deletion.DO_NOTHING, to_field="asin", db_column="asin", db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ts = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'amazon_scrape_tasks'

from __future__ import unicode_literals

from django.db import models


class AmazonItem(models.Model):
    STATUS_INACTIVE = 0 # asin is not available any longer (amazon link not available)
    STATUS_ACTIVE = 1

    asin = models.CharField(max_length=32, unique=True)
    url = models.TextField()
    category = models.CharField(max_length=255, blank=True, null=True)
    title = models.TextField()
    price = models.DecimalField(max_digits=15, decimal_places=2)
    market_price = models.DecimalField(max_digits=15, decimal_places=2)
    quantity = models.SmallIntegerField(blank=True, null=True, default=0)
    features = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    review_count = models.SmallIntegerField(blank=True, null=True, default=0)
    avg_rating = models.FloatField(blank=True, null=True, default=0)
    is_fba = models.BooleanField(default=0)
    is_addon = models.BooleanField(default=0)
    is_pantry = models.BooleanField(default=0)
    merchant_id = models.CharField(max_length=32, blank=True, null=True)
    merchant_name = models.CharField(max_length=100, blank=True, null=True)
    brand_name = models.CharField(max_length=100, blank=True, null=True)
    status = models.SmallIntegerField(blank=True, null=True, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ts = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'amazon_items'


class AmazonItemPicture(models.Model):
    amazon_item = models.ForeignKey('AmazonItem', on_delete=models.CASCADE, to_field="asin", db_column="asin")
    picture_url = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ts = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.picture_url

    class Meta:
        db_table = 'amazon_item_pictures'


class AmazonItemOffer(models.Model):
    amazon_item = models.ForeignKey('AmazonItem', on_delete=models.deletion.DO_NOTHING, blank=True, null=True, to_field="asin", db_column="asin")
    price = models.DecimalField(max_digits=15, decimal_places=2)
    quantity = models.SmallIntegerField(blank=True, null=True, default=0)
    is_fba = models.BooleanField(default=0)
    merchant_id = models.CharField(max_length=32, blank=True, null=True)
    merchant_name = models.CharField(max_length=100, blank=True, null=True)
    revision = models.IntegerField(blank=True, null=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ts = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'amazon_item_offers'


class EbayItemCategory(models.Model):
    category_id = models.CharField(max_length=100, unique=True)
    category_level = models.SmallIntegerField()
    category_name = models.CharField(max_length=100)
    category_parent_id = models.CharField(max_length=100)
    auto_pay_enabled = models.BooleanField(default=1)
    best_offer_enabled = models.BooleanField(default=1)
    leaf_category = models.BooleanField(default=0)

    def __str__(self):
        return self.category_name

    class Meta:
        db_table = 'ebay_product_categories'


class AToECategoryMap(models.Model):
    amazon_category = models.CharField(max_length=255)
    ebay_item_category = models.ForeignKey('EbayItemCategory', on_delete=models.deletion.DO_NOTHING, blank=True, null=True, to_field="category_id", db_column="ebay_category_id")
    ebay_category_name = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ts = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'a_to_e_category_maps'


class AmazonBestseller(models.Model):
    bestseller_category = models.CharField(max_length=255)
    bestseller_category_url = models.TextField()
    rank = models.SmallIntegerField()
    amazon_item = models.ForeignKey('AmazonItem', on_delete=models.deletion.DO_NOTHING, blank=True, null=True, to_field="asin", db_column="asin")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ts = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'amazon_bestsellers'

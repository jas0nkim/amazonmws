from __future__ import unicode_literals

from django.db import models


class AmazonItem(models.Model):
    asin = models.CharField(max_length=32)
    url = models.TextField()
    category = models.CharField(max_length=255, blank=True, null=True)
    title = models.TextField()
    price = models.DecimalField(max_digits=15, decimal_places=2)
    market_price = models.DecimalField(max_digits=15, decimal_places=2)
    quantity = models.SmallIntegerField(blank=True, null=True)
    features = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    review_count = models.SmallIntegerField(blank=True, null=True)
    avg_rating = models.FloatField(blank=True, null=True)
    is_fba = models.SmallIntegerField(blank=True, null=True)
    is_addon = models.SmallIntegerField(blank=True, null=True)
    is_pantry = models.SmallIntegerField(blank=True, null=True)
    merchant_id = models.CharField(max_length=32, blank=True, null=True)
    merchant_name = models.CharField(max_length=100, blank=True, null=True)
    brand_name = models.CharField(max_length=100, blank=True, null=True)
    status = models.SmallIntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'zz__amazon_items'


class AmazonItemPicture(models.Model):
    asin = models.CharField(max_length=32)
    picture_url = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'zz__amazon_item_pictures'


class AmazonItemOffer(models.Model):
    asin = models.CharField(max_length=32, blank=True, null=True)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    quantity = models.SmallIntegerField(blank=True, null=True)
    is_fba = models.SmallIntegerField(blank=True, null=True)
    merchant_id = models.CharField(max_length=32, blank=True, null=True)
    merchant_name = models.CharField(max_length=100, blank=True, null=True)
    revision = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'zz__amazon_item_offers'


class AToECategoryMap(models.Model):
    amazon_category = models.CharField(max_length=255)
    ebay_category_id = models.CharField(max_length=100, blank=True, null=True)
    ebay_category_name = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'zz__a_to_e_category_maps'


class AmazonBestseller(models.Model):
    bestseller_category = models.CharField(max_length=255)
    bestseller_category_url = models.TextField()
    rank = models.SmallIntegerField()
    asin = models.CharField(max_length=32, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'zz__amazon_bestsellers'

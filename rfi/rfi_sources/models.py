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
        db_table = 'zz__amazon_items'


class AmazonItemPicture(models.Model):
    asin = models.ForeignKey('AmazonItem', on_delete=models.CASCADE, to_field="asin")
    picture_url = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'zz__amazon_item_pictures'


class AmazonItemOffer(models.Model):
    asin = models.ForeignKey('AmazonItem', on_delete=models.deletion.DO_NOTHING, to_field="asin")
    price = models.DecimalField(max_digits=15, decimal_places=2)
    quantity = models.SmallIntegerField(blank=True, null=True)
    is_fba = models.SmallIntegerField(blank=True, null=True)
    merchant_id = models.CharField(max_length=32, blank=True, null=True)
    merchant_name = models.CharField(max_length=100, blank=True, null=True)
    revision = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'zz__amazon_item_offers'


class EbayProductCategory(models.Model):
    category_id = models.CharField(max_length=100, unique=True)
    category_level = models.SmallIntegerField()
    category_name = models.CharField(max_length=100)
    category_parent_id = models.CharField(max_length=100)
    auto_pay_enabled = models.IntegerField(blank=True, null=True)
    best_offer_enabled = models.IntegerField(blank=True, null=True)
    leaf_category = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'ebay_product_categories'


class AToECategoryMap(models.Model):
    amazon_category = models.CharField(max_length=255)
    ebay_category_id = models.ForeignKey('EbayProductCategory', on_delete=models.deletion.DO_NOTHING, to_field="category_id")
    ebay_category_name = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'zz__a_to_e_category_maps'


class AmazonBestseller(models.Model):
    bestseller_category = models.CharField(max_length=255)
    bestseller_category_url = models.TextField()
    rank = models.SmallIntegerField()
    asin = models.ForeignKey('AmazonItem', on_delete=models.deletion.DO_NOTHING, to_field="asin")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'zz__amazon_bestsellers'

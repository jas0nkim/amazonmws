from __future__ import unicode_literals

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from django.db import models

from amazonmws import settings as amazonmws_settings

class AmazonItem(models.Model):
    STATUS_INACTIVE = 0 # asin is not available any longer (amazon link not available)
    STATUS_ACTIVE = 1

    asin = models.CharField(max_length=32, unique=True, db_index=True)
    parent_asin = models.CharField(max_length=32, db_index=True, blank=True, null=True)
    url = models.TextField()
    category = models.CharField(max_length=255, blank=True, null=True)
    title = models.TextField()
    price = models.DecimalField(max_digits=15, decimal_places=2)
    market_price = models.DecimalField(max_digits=15, decimal_places=2)
    quantity = models.SmallIntegerField(blank=True, null=True, default=0)
    features = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    specifications = models.TextField(blank=True, null=True)
    variation_specifics = models.CharField(max_length=255, blank=True, null=True)
    review_count = models.SmallIntegerField(blank=True, null=True, default=0)
    avg_rating = models.FloatField(blank=True, null=True, default=0)
    is_fba = models.BooleanField(default=0)
    is_addon = models.BooleanField(default=0)
    is_pantry = models.BooleanField(default=0)
    has_sizechart = models.BooleanField(default=0)
    merchant_id = models.CharField(max_length=32, blank=True, null=True)
    merchant_name = models.CharField(max_length=100, blank=True, null=True)
    brand_name = models.CharField(max_length=100, blank=True, null=True)
    status = models.SmallIntegerField(blank=True, null=True, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ts = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def __unicode__(self):
        return u'{}'.format(self.title)

    def is_listable(self, ebay_store=None, excl_brands=[]):
        """ - check status
            - check is FBA
            - check is add-on
            - check is pantry
            - check quantity
        """
        if self.status != self.STATUS_ACTIVE:
            return False
        if float(self.price) < 1.00:
            return False
        if not self.is_fba:
            return False
        if self.is_addon:
            return False
        if self.is_pantry:
            return False
        if self.quantity < amazonmws_settings.AMAZON_MINIMUM_QUANTITY_FOR_LISTING:
            return False
        if ebay_store and ebay_store.__class__.__name__ == 'EbayStore':
            if self.price < float(ebay_store.listing_min_dollar) if ebay_store.listing_min_dollar else 0.00:
                return False
            if self.price > float(ebay_store.listing_max_dollar) if ebay_store.listing_max_dollar else 999999999.99:
                return False
        if len(excl_brands) > 0:
            for excl_brand in excl_brands:
                if excl_brand.__class__.__name__ == 'ExclBrand' and self.brand_name == excl_brand.brand_name:
                    return False
        return True

    def is_a_variation(self):
        if self.asin == self.parent_asin:
            return False
        return True

    class Meta:
        db_table = 'amazon_items'


class AmazonItemPicture(models.Model):
    asin = models.CharField(max_length=32, db_index=True)
    picture_url = models.CharField(max_length=255, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ts = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.picture_url

    class Meta:
        db_table = 'amazon_item_pictures'


class AmazonItemPrice(models.Model):
    asin = models.CharField(max_length=32, db_index=True)
    parent_asin = models.CharField(max_length=32, db_index=True, blank=True, null=True)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ts = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.asin

    class Meta:
        db_table = 'amazon_item_prices'


class AmazonItemMarketPrice(models.Model):
    asin = models.CharField(max_length=32, db_index=True)
    parent_asin = models.CharField(max_length=32, db_index=True, blank=True, null=True)
    market_price = models.DecimalField(max_digits=15, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ts = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.asin

    class Meta:
        db_table = 'amazon_item_market_prices'


class AmazonItemQuantity(models.Model):
    asin = models.CharField(max_length=32, db_index=True)
    parent_asin = models.CharField(max_length=32, db_index=True, blank=True, null=True)
    quantity = models.SmallIntegerField(blank=True, null=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ts = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.asin

    class Meta:
        db_table = 'amazon_item_quantites'


class AmazonItemTitle(models.Model):
    asin = models.CharField(max_length=32, db_index=True)
    parent_asin = models.CharField(max_length=32, db_index=True, blank=True, null=True)
    title = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ts = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.asin

    class Meta:
        db_table = 'amazon_item_titles'


class AmazonItemDescription(models.Model):
    asin = models.CharField(max_length=32, db_index=True)
    parent_asin = models.CharField(max_length=32, db_index=True, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ts = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.asin

    class Meta:
        db_table = 'amazon_item_descriptions'


class AmazonItemFeature(models.Model):
    asin = models.CharField(max_length=32, db_index=True)
    parent_asin = models.CharField(max_length=32, db_index=True, blank=True, null=True)
    features = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ts = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.asin

    class Meta:
        db_table = 'amazon_item_features'


class AmazonItemApparel(models.Model):
    parent_asin = models.CharField(max_length=32, db_index=True)
    size_chart = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ts = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.parent_asin

    class Meta:
        db_table = 'amazon_item_apparels'


class AmazonItemOffer(models.Model):
    asin = models.CharField(max_length=32, db_index=True)
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
    category_id = models.CharField(max_length=100, unique=True, db_index=True)
    category_level = models.SmallIntegerField()
    category_name = models.CharField(max_length=100)
    category_parent_id = models.CharField(max_length=100, db_index=True)
    auto_pay_enabled = models.BooleanField(default=1)
    best_offer_enabled = models.BooleanField(default=1)
    leaf_category = models.BooleanField(default=0)

    def __str__(self):
        return self.category_name

    class Meta:
        db_table = 'ebay_product_categories'


class AToECategoryMap(models.Model):
    amazon_category = models.CharField(max_length=255, db_index=True)
    ebay_category_id = models.CharField(max_length=100, blank=True, null=True, db_index=True)
    ebay_category_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="eBay Category")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ts = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'a_to_e_category_maps'
        verbose_name = 'Amazon-eBay Category Map'


class AmazonBestseller(models.Model):
    bestseller_category = models.CharField(max_length=255, db_index=True)
    bestseller_category_url = models.TextField()
    rank = models.SmallIntegerField(db_index=True)
    asin = models.CharField(max_length=32, db_index=True)
    review_count = models.SmallIntegerField(blank=True, null=True, default=0)
    avg_rating = models.FloatField(blank=True, null=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ts = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'amazon_bestsellers'

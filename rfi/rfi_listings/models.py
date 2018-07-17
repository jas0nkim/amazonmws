from __future__ import unicode_literals

from django.db import models
from django.core.exceptions import MultipleObjectsReturned

from rfi_sources.models import AmazonItem
from rfi_account_profiles.models import EbayStore
from rfi.fields import RfiForeignKey


class EbayItem(models.Model):
    # EbayItem.status values
    STATUS_INACTIVE = 0 # ended item
    STATUS_ACTIVE = 1 # active item
    STATUS_OUT_OF_STOCK = 2 # out of stock item

    ebay_store = RfiForeignKey(EbayStore, on_delete=models.CASCADE, db_index=True)
    asin = models.CharField(max_length=32, db_index=True, blank=True, null=True)
    ebid = models.CharField(max_length=100, unique=True, db_index=True)
    ebay_category_id = models.CharField(max_length=100, null=True, blank=True, db_index=True)
    eb_price = models.DecimalField(max_digits=15, decimal_places=2)
    quantity = models.SmallIntegerField(blank=True, null=True, default=0)
    status = models.SmallIntegerField(blank=True, null=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ts = models.DateTimeField(auto_now=True)

    amazon_item = None

    def __init__(self, *args, **kwargs):
        super(EbayItem, self).__init__(*args, **kwargs)
        self.__set_amazon_item()

    def __set_amazon_item(self):
        self.amazon_item = self.get_amazon_item()

    def get_amazon_item(self):
        try:
            _amazon_items = AmazonItem.objects.filter(parent_asin=self.asin)
            if _amazon_items.count() > 0:
                return _amazon_items.first()
            else:
                raise Exception()
        except Exception:
            pass
        try:
            return AmazonItem.objects.get(asin=self.asin)
        except MultipleObjectsReturned as e:
            return None
        except AmazonItem.DoesNotExist as e:
            return None

    class Meta:
        db_table = 'ebay_items'


class EbayItemVariation(models.Model):
    ebay_item = RfiForeignKey('EbayItem', on_delete=models.CASCADE, db_index=True)
    ebid = models.CharField(max_length=100, db_index=True)
    asin = models.CharField(max_length=32, db_index=True)
    specifics = models.CharField(max_length=255, null=True, blank=True)
    eb_price = models.DecimalField(max_digits=15, decimal_places=2)
    quantity = models.SmallIntegerField(blank=True, null=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ts = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ebay_item_variations'


class EbayPicture(models.Model):
    source_picture_url = models.CharField(max_length=255, db_index=True)
    picture_url = models.CharField(max_length=255, db_index=True)
    base_url = models.CharField(max_length=255, db_index=True)
    full_url = models.CharField(max_length=255, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ts = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.picture_url

    class Meta:
        db_table = 'ebay_pictures'


class EbayPictureSetMember(models.Model):
    ebay_picture = RfiForeignKey('EbayPicture', on_delete=models.CASCADE, db_index=True)
    member_url = models.CharField(max_length=255, db_index=True)
    picture_height = models.SmallIntegerField(blank=True, null=True, default=0)
    picture_width = models.SmallIntegerField(blank=True, null=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ts = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.member_url

    class Meta:
        db_table = 'ebay_picture_set_members'


class EbayCategoryFeatures(models.Model):
    ebay_category_id = models.CharField(max_length=100, unique=True, db_index=True)
    ebay_category_name = models.CharField(max_length=255, blank=True, null=True)
    upc_enabled = models.CharField(max_length=100, blank=True, null=True)
    variations_enabled = models.BooleanField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ts = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ebay_category_features'


class EbayItemStat(models.Model):
    ebay_store = RfiForeignKey(EbayStore, on_delete=models.CASCADE, db_index=True)
    ebid = models.CharField(max_length=100, db_index=True)
    clicks = models.IntegerField(blank=True, null=True, default=0)
    watches = models.IntegerField(blank=True, null=True, default=0)
    solds = models.IntegerField(blank=True, null=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ts = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ebay_item_stats'


class EbayItemPopularity(models.Model):
    # EbayItemPopularity.popularity values
    POPULARITY_POPULAR = 1 # popular items
    POPULARITY_NORMAL = 2 # normal items
    POPULARITY_SLOW = 3 # slow items

    ebay_store = RfiForeignKey(EbayStore, on_delete=models.CASCADE, db_index=True)
    ebid = models.CharField(max_length=100, db_index=True)
    parent_asin = models.CharField(max_length=32, db_index=True, blank=True, null=True)
    popularity = models.SmallIntegerField(default=2, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ts = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ebay_item_popularities'


class EbayItemLastReviseAttempted(models.Model):
    ebay_store = RfiForeignKey(EbayStore, on_delete=models.CASCADE, db_index=True)
    ebid = models.CharField(max_length=100, db_index=True)
    ebay_item_variation_id = models.IntegerField(default=0, db_index=True)
    asin = models.CharField(max_length=32, db_index=True, blank=True, null=True)
    parent_asin = models.CharField(max_length=32, db_index=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ts = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ebay_item_last_revise_attempted'


class EbayStoreCategory(models.Model):
    ebay_store = RfiForeignKey(EbayStore, on_delete=models.CASCADE, db_index=True)
    category_id = models.BigIntegerField(unique=True, db_index=True)
    parent_category_id = models.BigIntegerField(blank=True, null=True, default=0)
    name = models.CharField(max_length=100, db_index=True)
    order = models.IntegerField(blank=True, null=True, default=0)
    level = models.IntegerField(blank=True, null=True, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ts = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ebay_store_categories'


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
    amazon_item = RfiForeignKey(AmazonItem, on_delete=models.deletion.DO_NOTHING, to_field="asin", db_column="asin", db_index=True)
    parent_asin = models.CharField(max_length=32, db_index=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ts = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'amazon_scrape_tasks'



""" NEW (Jun/22/2018) - eBay Inventory API related
"""
class EbayInventoryLocation(models.Model):
    # EbayInventoryLocation.status values
    STATUS_DISABLED = 0 # disabled location
    STATUS_ENABLED = 1 # enabled location

    ebay_store = RfiForeignKey(EbayStore, on_delete=models.CASCADE, db_index=True)
    merchant_location_key = models.CharField(max_length=255, db_index=True)
    address_country = models.CharField(max_length=32, blank=True, null=True)
    status = models.SmallIntegerField(blank=True, null=True, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ts = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ebay_inventory_locations'


class EbayInventoryItem(models.Model):
    ebay_store = RfiForeignKey(EbayStore, on_delete=models.CASCADE, db_index=True)
    sku = models.CharField(max_length=100, db_index=True, unique=True)
    ship_to_location_availability_quantity = models.SmallIntegerField(blank=True, null=True, default=0)
    title = models.TextField()
    description = models.TextField(blank=True, null=True)
    variation_specifics = models.TextField(blank=True, null=True)
    aspects = models.TextField(blank=True, null=True)
    image_urls = models.TextField(blank=True, null=True)
    inventory_item_group_keys = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ts = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ebay_inventory_items'


class EbayInventoryItemGroup(models.Model):
    ebay_store = RfiForeignKey(EbayStore, on_delete=models.CASCADE, db_index=True)
    inventory_item_group_key = models.CharField(max_length=100, db_index=True, unique=True)
    title = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    common_aspects = models.TextField(blank=True, null=True)
    image_urls = models.TextField(blank=True, null=True)
    variant_skus = models.TextField(blank=True, null=True)
    aspects_image_varies_by = models.TextField(blank=True, null=True)
    varies_by_specifications = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ts = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ebay_inventory_item_groups'


class EbayInventoryItemEbayInventoryItemGroup(models.Model):
    ebay_inventory_item = RfiForeignKey('EbayInventoryItem', on_delete=models.deletion.DO_NOTHING, blank=True, null=True, to_field="sku", db_column="sku", db_index=True)
    ebay_inventory_item_group = RfiForeignKey('EbayInventoryItemGroup', on_delete=models.deletion.DO_NOTHING, blank=True, null=True, to_field="inventory_item_group_key", db_column="inventory_item_group_key", db_index=True)

    class Meta:
        db_table = 'ebay_inventory_items_ebay_inventory_item_groups'


class EbayOffer(models.Model):
    # EbayOffer.status values
    STATUS_UNPUBLISHED = 0 # unpublished offer
    STATUS_PUBLISHED = 1 # published offer

    ebay_store = RfiForeignKey(EbayStore, on_delete=models.CASCADE, db_index=True)
    offer_id = models.CharField(max_length=100, db_index=True)
    listing_id = models.CharField(max_length=100, blank=True, null=True, db_index=True)
    available_quantity = models.SmallIntegerField(blank=True, null=True, default=0)
    ebay_category_id = models.CharField(max_length=100, null=True, blank=True, db_index=True)
    payment_policy_id = models.CharField(max_length=100, null=True, blank=True)
    return_policy_id = models.CharField(max_length=100, null=True, blank=True)
    fulfillment_policy_id = models.CharField(max_length=100, null=True, blank=True)
    merchant_location_key = models.CharField(max_length=255, db_index=True)
    original_retail_price = models.DecimalField(max_digits=15, decimal_places=2)
    original_retail_price_currency = models.CharField(max_length=32, blank=True, null=True)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    price_currency = models.CharField(max_length=32, blank=True, null=True)
    quantity_limit_per_buyer = models.SmallIntegerField(blank=True, null=True)
    store_category_names = models.TextField(blank=True, null=True)
    sku = models.CharField(max_length=100, db_index=True)
    marketplace_id = models.CharField(max_length=32, db_index=True)
    listing_format = models.CharField(max_length=32, db_index=True)
    status = models.SmallIntegerField(blank=True, null=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ts = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ebay_offers'


# class EbayOfferListing(models.Model):
#     ebay_store = RfiForeignKey(EbayStore, on_delete=models.CASCADE, db_index=True)
#     listing_id = models.CharField(max_length=100, db_index=True)
#     offer_id = models.CharField(max_length=100, blank=True, null=True)
#     inventory_item_group_key = models.CharField(max_length=100, blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     ts = models.DateTimeField(auto_now=True)

#     class Meta:
#         db_table = 'ebay_offer_listings'


from __future__ import unicode_literals

from django.db import models


class EbayStore(models.Model):
    email = models.CharField(max_length=100, db_index=True)
    username = models.CharField(max_length=100, unique=True, db_index=True)
    password = models.CharField(max_length=100, blank=True, null=True)
    token = models.TextField(blank=True, null=True)
    token_expiration = models.DateField(blank=True, null=True)
    store_name = models.CharField(max_length=100, blank=True, null=True)
    paypal_username = models.CharField(max_length=100)
    margin_percentage = models.SmallIntegerField(blank=True, null=True, default=10)
    margin_min_dollar = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True, default='0.00')
    margin_max_dollar = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True, default='10.00')
    listing_min_dollar = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    listing_max_dollar = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    policy_shipping = models.TextField(blank=True, null=True)
    policy_payment = models.TextField(blank=True, null=True)
    policy_return = models.TextField(blank=True, null=True)
    returns_accepted = models.BooleanField(default=1)
    use_salestax_table = models.BooleanField(default=0)
    fixed_salestax_percentage = models.SmallIntegerField(blank=True, null=True, default=10)
    item_description_template = models.TextField(blank=True, null=True)
    feedback_comment = models.TextField(blank=True, null=True)
    message_on_shipping_subject = models.TextField(blank=True, null=True)
    message_on_shipping_body = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ts = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'ebay_stores'


class AmazonAccount(models.Model):
    ebay_stores = models.ManyToManyField('EbayStore')
    email = models.CharField(max_length=100, db_index=True)
    password = models.CharField(max_length=100)
    billing_postal = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ts = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'amazon_accounts'

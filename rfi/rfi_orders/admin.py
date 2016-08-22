from django.contrib import admin
from models import *


class AmazonOrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'amazon_item', 'total', 'carrier', 'tracking_number',)
    list_filter = ('amazon_account',)
    raw_id_fields = ("amazon_item",)


class EbayOrderAdmin(admin.ModelAdmin):
    list_display = ('record_number', 'order_id', 'total_price', 'creation_time',)
    list_filter = ('ebay_store',)


class EbayOrderAmazonOrderAdmin(admin.ModelAdmin):
    list_display = ('ebay_order', 'amazon_order',)


admin.site.register(AmazonOrder, AmazonOrderAdmin)
admin.site.register(EbayOrder, EbayOrderAdmin)
admin.site.register(EbayOrderAmazonOrder, EbayOrderAmazonOrderAdmin)

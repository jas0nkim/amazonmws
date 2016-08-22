from django.contrib import admin
from models import *


class AmazonOrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'amazon_item', 'total', 'carrier', 'tracking_number',)
    list_filter = ('amazon_account',)


class EbayOrderAdmin(admin.ModelAdmin):
    list_display = ('record_number', 'order_id', 'total_price', 'creation_time',)
    list_filter = ('ebay_store',)


admin.site.register(AmazonOrder, AmazonOrderAdmin)
admin.site.register(EbayOrder, EbayOrderAdmin)

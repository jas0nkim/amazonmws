from django.contrib import admin
from models import *


class AmazonOrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'total_cost', 'created_at', 'carrier', 'tracking_number',)
    list_filter = ('amazon_account',)
    # raw_id_fields = ("ordered_items",)
    search_fields = ['order_id', ]

    def total_cost(self, obj):
        return "${}".format(obj.total) if obj.total else ""


class EbayOrderAdmin(admin.ModelAdmin):
    list_display = ('record_number', 'order_id', 'total_amount', 'creation_time',)
    list_filter = ('ebay_store',)
    search_fields = ['order_id', 'record_number', ]

    def total_amount(self, obj):
        return "${}".format(obj.total_price) if obj.total_price else ""


class EbayOrderAmazonOrderAdmin(admin.ModelAdmin):
    list_display = ('ebay_order', 'amazon_order',)
    search_fields = ['amazon_order_id', 'ebay_order_id', ]


class EbayOrderShippingAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'carrier', 'tracking_number',)
    list_filter = ('carrier',)
    search_fields = ['order_id', 'carrier', 'tracking_number', ]


admin.site.register(AmazonOrder, AmazonOrderAdmin)
admin.site.register(EbayOrder, EbayOrderAdmin)
admin.site.register(EbayOrderAmazonOrder, EbayOrderAmazonOrderAdmin)
admin.site.register(EbayOrderShipping, EbayOrderShippingAdmin)

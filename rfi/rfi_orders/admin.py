from django.contrib import admin
from models import *


class AmazonOrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'total_cost', 'created_at', 'carrier', 'tracking_number', 'ordered_items',)
    list_filter = ('amazon_account',)
    # raw_id_fields = ("ordered_items",)

    def total_cost(self, obj):
        return "${}".format(obj.total) if obj.total else ""


class EbayOrderAdmin(admin.ModelAdmin):
    list_display = ('record_number', 'order_id', 'total_amount', 'creation_time',)
    list_filter = ('ebay_store',)

    def total_amount(self, obj):
        return "${}".format(obj.total_price) if obj.total_price else ""


class EbayOrderAmazonOrderAdmin(admin.ModelAdmin):
    list_display = ('ebay_order', 'amazon_order',)


admin.site.register(AmazonOrder, AmazonOrderAdmin)
admin.site.register(EbayOrder, EbayOrderAdmin)
admin.site.register(EbayOrderAmazonOrder, EbayOrderAmazonOrderAdmin)

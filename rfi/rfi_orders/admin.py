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


class EbayOrderReturnAdmin(admin.ModelAdmin):
    list_display = ('return_id', 'item_id', 'buyer_username', 'refunded_amount', 'status', 'state', 'creation_time')
    list_filter = ('status', 'state')
    search_fields = ['return_id', 'item_id', 'buyer_username', ]
    ordering = ('-return_id', )

    def refunded_amount(self, obj):
        return "${}".format(obj.act_refund_amount) if obj.act_refund_amount else "-"


class AmazonOrderReturnAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'asin', 'return_id', 'refunded_dollar', 'refunded_on' 'status')
    list_filter = ('amazon_account', 'status')
    search_fields = ['order_id', 'asin', ]
    ordering = ('-ebay_return_id', )

    def refunded_dollar(self, obj):
        return "${}".format(obj.refunded_amount) if obj.refunded_amount else "-"

    def refunded_on(self, obj):
        return obj.refunded_date if obj.refunded_date else "-"


admin.site.register(AmazonOrder, AmazonOrderAdmin)
admin.site.register(EbayOrder, EbayOrderAdmin)
admin.site.register(EbayOrderAmazonOrder, EbayOrderAmazonOrderAdmin)
admin.site.register(EbayOrderShipping, EbayOrderShippingAdmin)
admin.site.register(EbayOrderReturn, EbayOrderReturnAdmin)
admin.site.register(AmazonOrderReturn, AmazonOrderReturnAdmin)

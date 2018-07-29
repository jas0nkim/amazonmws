from __future__ import unicode_literals

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from django.contrib import admin

from amazonmws import settings as amazonmws_settings

from models import *


class BaseCountedListFilter(admin.SimpleListFilter):

    def lookups(self, request, model_admin):
        qs = model_admin.get_queryset(request)
        values = qs.order_by().values_list(self.parameter_name, flat=True).distinct()
        for v in values:
            yield (v, "{} ({})".format(v, qs.filter(**{ self.parameter_name: v, }).count()))

    def queryset(self, request, queryset):
        return queryset.filter(**{ self.parameter_name: self.value(), }).order_by('-updated_at')


class EbayErrorCodeFilter(BaseCountedListFilter):
    title = 'error code'
    parameter_name = 'error_code'

    def lookups(self, request, model_admin):
        return super(EbayErrorCodeFilter, self).lookups(request, model_admin)

    def queryset(self, request, queryset):
        return super(EbayErrorCodeFilter, self).queryset(request, queryset)


class EbayTradingApiErrorAdmin(admin.ModelAdmin):
    list_display = ('error_code', 'desc', 'asin_link', 'ebid_link', 'count', )
    list_filter = ('severity_code', 'trading_api', EbayErrorCodeFilter,)
    search_fields = ['error_code', 'asin', 'ebid', ]

    def desc(self, obj):
        return obj.description[:70] + "..." if len(obj.description) > 70 else obj.description

    def asin_link(self, obj):
        return "{asin} <a href=\"{url}\" target=\"_blank\">Link</a>".format(
            url=amazonmws_settings.AMAZON_ITEM_VARIATION_LINK_FORMAT % obj.asin,
            asin=obj.asin) if obj.asin else ""

    asin_link.allow_tags = True

    def ebid_link(self, obj):
        return "{ebid} <a href=\"{url}\" target=\"_blank\">Link</a>".format(
            url=amazonmws_settings.EBAY_ITEM_LINK_FORMAT % obj.ebid,
            ebid=obj.ebid) if obj.ebid else ""

    ebid_link.allow_tags = True


class AmazonErrorCodeFilter(BaseCountedListFilter):
    title = 'error code'
    parameter_name = 'error_code'

    def lookups(self, request, model_admin):
        return super(AmazonErrorCodeFilter, self).lookups(request, model_admin)

    def queryset(self, request, queryset):
        return super(AmazonErrorCodeFilter, self).queryset(request, queryset)


class AmazonScrapeErrorAdmin(admin.ModelAdmin):
    list_display = ('asin_link', 'error_code', 'description', 'sys_err_msg', 'count', )
    list_filter = ('http_status', AmazonErrorCodeFilter, )
    search_fields = ['error_code', 'asin', ]

    def sys_err_msg(self, obj):
        return obj.system_error_message[:70] + "..." if len(obj.system_error_message) > 70 else obj.system_error_message

    def asin_link(self, obj):
        return "{asin} <a href=\"{url}\" target=\"_blank\">Link</a>".format(
            url=amazonmws_settings.AMAZON_ITEM_VARIATION_LINK_FORMAT % obj.asin,
            asin=obj.asin) if obj.asin else ""

    asin_link.allow_tags = True


admin.site.register(EbayTradingApiError, EbayTradingApiErrorAdmin)
admin.site.register(AmazonScrapeError, AmazonScrapeErrorAdmin)
from __future__ import unicode_literals

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from django.contrib import admin

from amazonmws import settings as amazonmws_settings

from models import *


class EbayTradingApiErrorAdmin(admin.ModelAdmin):
    list_display = ('error_code', 'desc', 'asin_link', 'ebid_link', 'count', )
    list_filter = ('severity_code', 'trading_api', 'error_code',)
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

admin.site.register(EbayTradingApiError, EbayTradingApiErrorAdmin)
from __future__ import unicode_literals

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from django.contrib import admin

from amazonmws import settings as amazonmws_settings

from models import *


class EbayTradingApiErrorAdmin(admin.ModelAdmin):
    list_display = ('message_id', 'error_code', 'asin_link', 'ebid_link',)
    list_filter = ('error_code',)
    search_fields = ['message_id', 'error_code', 'asin', 'ebid',]

    def asin_link(self, obj):
        return "<a href=\"{url}\" target=\"_blank\">{asin}</a>".format(
            url=amazonmws_settings.AMAZON_ITEM_VARIATION_LINK_FORMAT % obj.asin,
            asin=obj.asin if obj.asin else "")

    asin_link.allow_tags = True

    def ebid_link(self, obj):
        return "<a href=\"{url}\" target=\"_blank\">{ebid}</a>".format(
            url=amazonmws_settings.EBAY_ITEM_LINK_FORMAT % obj.ebid,
            ebid=obj.ebid if obj.ebid else "")

    ebid_link.allow_tags = True

admin.site.register(EbayTradingApiError, EbayTradingApiErrorAdmin)
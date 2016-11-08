import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from django.contrib import admin
from django.utils.html import format_html
from models import *

from amazonmws import settings as amazonmws_settings


class AToECategoryMapAdmin(admin.ModelAdmin):
    list_display = ('amazon_category', 'ebay_category_name', 'ebay_category_link', )
    search_fields = ['amazon_category', 'ebay_category_name', 'ebay_category_id', ]

    def ebay_category_link(self, obj):
        return format_html("<a href=\"{url}\" target=\"_blank\">{category_id}</a>", 
            url=amazonmws_settings.EBAY_CATEGORY_LINK_FORMAT.format(category_id=obj.ebay_category_id),
            category_id=obj.ebay_category_id)

    ebay_category_link.short_description = "eBay Category Link"

admin.site.register(AToECategoryMap, AToECategoryMapAdmin)
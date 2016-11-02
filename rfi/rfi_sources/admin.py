from django.contrib import admin
from models import *

class AToECategoryMapAdmin(admin.ModelAdmin):
    list_display = ('amazon_category', 'ebay_category_name', )
    search_fields = ['amazon_category', 'ebay_category_name', ]


admin.site.register(AToECategoryMap, AToECategoryMapAdmin)
from django.contrib import admin
from models import *

class EbayStoreAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'created_at',)
    list_filter = ('username',)


class AmazonAccountAdmin(admin.ModelAdmin):
    list_display = ('email', )
    list_filter = ('ebay_stores',)


admin.site.register(EbayStore, EbayStoreAdmin)
admin.site.register(AmazonAccount, AmazonAccountAdmin)

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from django.contrib import admin
from models import *


class ExclBrandAdmin(admin.ModelAdmin):
    list_display = ('brand_name', 'category', 'created_at', )
    search_fields = ['brand_name', ]

admin.site.register(ExclBrand, ExclBrandAdmin)
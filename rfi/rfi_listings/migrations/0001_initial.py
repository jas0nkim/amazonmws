# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-05 16:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import rfi.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('rfi_account_profiles', '0001_initial'),
        ('rfi_sources', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EbayItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ebid', models.CharField(db_index=True, max_length=100, unique=True)),
                ('eb_price', models.DecimalField(decimal_places=2, max_digits=15)),
                ('quantity', models.SmallIntegerField(blank=True, default=0, null=True)),
                ('status', models.SmallIntegerField(blank=True, default=0, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('ts', models.DateTimeField(auto_now=True)),
                ('amazon_item', rfi.fields.RfiForeignKey(db_column='asin', on_delete=django.db.models.deletion.DO_NOTHING, to='rfi_sources.AmazonItem', to_field='asin')),
                ('ebay_item_category', rfi.fields.RfiForeignKey(db_column='ebay_category_id', on_delete=django.db.models.deletion.DO_NOTHING, to='rfi_sources.EbayItemCategory', to_field='category_id')),
                ('ebay_store', rfi.fields.RfiForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rfi_account_profiles.EbayStore')),
            ],
            options={
                'db_table': 'ebay_items',
            },
        ),
        migrations.CreateModel(
            name='EbayStorePreferredCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_type', models.CharField(choices=[('amazon', 'amazon'), ('amazon_bestseller', 'amazon_bestseller')], default='amazon', max_length=17)),
                ('category_name', models.CharField(max_length=255)),
                ('max_items', models.IntegerField(blank=True, default=0, null=True)),
                ('priority', models.SmallIntegerField(blank=True, default=0, null=True)),
                ('status', models.SmallIntegerField(blank=True, default=1, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('ts', models.DateTimeField(auto_now=True)),
                ('ebay_store', rfi.fields.RfiForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rfi_account_profiles.EbayStore')),
            ],
            options={
                'db_table': 'ebay_store_preferred_categories',
            },
        ),
        migrations.CreateModel(
            name='ExclBrand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand_name', models.CharField(db_index=True, max_length=100)),
                ('category', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('ts', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'excl_brands',
            },
        ),
    ]
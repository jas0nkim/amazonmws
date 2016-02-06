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
        ('rfi_listings', '0001_initial'),
        ('rfi_sources', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EbayNotificationError',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('correlation_id', models.CharField(db_index=True, max_length=100)),
                ('event_name', models.CharField(blank=True, max_length=100, null=True)),
                ('recipient_user_id', models.CharField(blank=True, db_index=True, max_length=100, null=True)),
                ('response', models.TextField()),
                ('error_code', models.IntegerField(blank=True, default=0, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('ts', models.DateTimeField(auto_now=True)),
                ('ebay_store', rfi.fields.RfiForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rfi_account_profiles.EbayStore')),
            ],
            options={
                'db_table': 'ebay_notification_errors',
            },
        ),
        migrations.CreateModel(
            name='EbayTradingApiError',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message_id', models.CharField(db_index=True, max_length=100)),
                ('trading_api', models.CharField(db_index=True, max_length=100)),
                ('request', models.TextField()),
                ('response', models.TextField()),
                ('error_code', models.IntegerField(blank=True, default=0, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('ts', models.DateTimeField(auto_now=True)),
                ('amazon_item', rfi.fields.RfiForeignKey(blank=True, db_column='asin', null=True, on_delete=django.db.models.deletion.CASCADE, to='rfi_sources.AmazonItem', to_field='asin')),
                ('ebay_item', rfi.fields.RfiForeignKey(blank=True, db_column='ebid', null=True, on_delete=django.db.models.deletion.CASCADE, to='rfi_listings.EbayItem', to_field='ebid')),
            ],
            options={
                'db_table': 'ebay_trading_api_errors',
            },
        ),
        migrations.CreateModel(
            name='ErrorEbayInvalidCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message_id', models.CharField(db_index=True, max_length=100)),
                ('amazon_category', models.CharField(db_index=True, max_length=255)),
                ('request', models.TextField()),
                ('status', models.SmallIntegerField(blank=True, default=0, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('ts', models.DateTimeField(auto_now=True)),
                ('amazon_item', rfi.fields.RfiForeignKey(db_column='asin', on_delete=django.db.models.deletion.CASCADE, to='rfi_sources.AmazonItem', to_field='asin')),
                ('ebay_category', rfi.fields.RfiForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='rfi_sources.EbayItemCategory', to_field='category_id')),
            ],
            options={
                'db_table': 'error_ebay_invalid_category',
            },
        ),
    ]
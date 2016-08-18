# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-08-18 18:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import rfi.fields


class Migration(migrations.Migration):

    dependencies = [
        ('rfi_account_profiles', '0002_ebaystore_margin_min_dollar'),
        ('rfi_orders', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EbayOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(db_index=True, max_length=100, unique=True)),
                ('record_number', models.IntegerField(default=0)),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=15)),
                ('shipping_cost', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
                ('buyer_email', models.CharField(db_index=True, max_length=100)),
                ('buyer_user_id', models.CharField(db_index=True, max_length=100)),
                ('buyer_status', models.CharField(blank=True, max_length=32, null=True)),
                ('buyer_shipping_name', models.CharField(max_length=100, null=True)),
                ('buyer_shipping_street1', models.CharField(blank=True, max_length=100, null=True)),
                ('buyer_shipping_street2', models.CharField(blank=True, max_length=100, null=True)),
                ('buyer_shipping_city_name', models.CharField(blank=True, max_length=100, null=True)),
                ('buyer_shipping_state_or_province', models.CharField(blank=True, max_length=100, null=True)),
                ('buyer_shipping_postal_code', models.CharField(blank=True, max_length=100, null=True)),
                ('buyer_shipping_country', models.CharField(blank=True, max_length=32, null=True)),
                ('buyer_shipping_phone', models.CharField(blank=True, max_length=100, null=True)),
                ('checkout_status', models.CharField(max_length=32)),
                ('creation_time', models.DateTimeField(blank=True, null=True)),
                ('paid_time', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('ts', models.DateTimeField(auto_now=True)),
                ('ebay_store', rfi.fields.RfiForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='rfi_account_profiles.EbayStore')),
            ],
            options={
                'db_table': 'ebay_orders',
            },
        ),
        migrations.CreateModel(
            name='EbayOrderAmazonOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'ebay_order_amazon_orders',
            },
        ),
        migrations.CreateModel(
            name='EbayOrderAutomationError',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('error_message', models.CharField(blank=True, max_length=255, null=True)),
                ('ebay_order', rfi.fields.RfiForeignKey(blank=True, db_column='ebay_order_id', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='rfi_orders.EbayOrder', to_field='order_id')),
            ],
            options={
                'db_table': 'ebay_order_automation_errors',
            },
        ),
        migrations.CreateModel(
            name='EbayOrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(db_index=True, max_length=100)),
                ('ebid', models.CharField(db_index=True, max_length=100)),
                ('transaction_id', models.CharField(db_index=True, max_length=100)),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('sku', models.CharField(blank=True, max_length=100, null=True)),
                ('quantity', models.SmallIntegerField(blank=True, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=15)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('ts', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'ebay_order_items',
            },
        ),
        migrations.CreateModel(
            name='EbayOrderShipping',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(db_index=True, max_length=100)),
                ('carrier', models.CharField(blank=True, max_length=100, null=True)),
                ('tracking_number', models.CharField(blank=True, max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('ts', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'ebay_order_shippings',
            },
        ),
        migrations.AlterField(
            model_name='amazonorder',
            name='order_id',
            field=models.CharField(db_index=True, max_length=100, unique=True),
        ),
        migrations.AddField(
            model_name='ebayorderamazonorder',
            name='amazon_order',
            field=rfi.fields.RfiForeignKey(blank=True, db_column='amazon_order_id', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='rfi_orders.AmazonOrder', to_field='order_id'),
        ),
        migrations.AddField(
            model_name='ebayorderamazonorder',
            name='ebay_order',
            field=rfi.fields.RfiForeignKey(blank=True, db_column='ebay_order_id', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='rfi_orders.EbayOrder', to_field='order_id'),
        ),
    ]

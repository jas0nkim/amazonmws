# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-23 18:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import rfi.fields


class Migration(migrations.Migration):

    dependencies = [
        ('rfi_account_profiles', '0005_ebaystore_policy_shipping_international'),
        ('rfi_orders', '0015_auto_20170223_1732'),
    ]

    operations = [
        migrations.CreateModel(
            name='AmazonOrderReturn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(db_index=True, max_length=100)),
                ('asin', models.CharField(blank=True, db_index=True, max_length=32, null=True)),
                ('return_id', models.CharField(blank=True, db_index=True, max_length=100, null=True)),
                ('ebay_return_id', models.CharField(blank=True, db_index=True, max_length=100, null=True)),
                ('quantity', models.SmallIntegerField(blank=True, null=True)),
                ('refunded_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
                ('carrier', models.CharField(blank=True, max_length=100, null=True)),
                ('tracking_number', models.CharField(blank=True, max_length=100, null=True)),
                ('rma', models.CharField(blank=True, max_length=100, null=True)),
                ('status', models.CharField(blank=True, max_length=100, null=True)),
                ('returned_date', models.DateField(blank=True, null=True)),
                ('refunded_date', models.DateField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('ts', models.DateTimeField(auto_now=True)),
                ('amazon_account', rfi.fields.RfiForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='rfi_account_profiles.AmazonAccount')),
            ],
            options={
                'db_table': 'amazon_order_returns',
            },
        ),
    ]

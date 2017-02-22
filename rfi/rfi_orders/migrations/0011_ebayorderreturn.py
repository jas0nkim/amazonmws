# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-14 18:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rfi_orders', '0010_ebayorder_payment_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='EbayOrderReturn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('return_id', models.CharField(db_index=True, max_length=100)),
                ('transaction_id', models.CharField(db_index=True, max_length=100)),
                ('item_id', models.CharField(db_index=True, max_length=100)),
                ('quantity', models.SmallIntegerField(blank=True, null=True)),
                ('buyer_username', models.CharField(db_index=True, max_length=100)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=15)),
                ('reason', models.CharField(blank=True, max_length=100, null=True)),
                ('carrier', models.CharField(blank=True, max_length=100, null=True)),
                ('tracking_number', models.CharField(blank=True, max_length=100, null=True)),
                ('rma', models.CharField(blank=True, max_length=100, null=True)),
                ('status', models.CharField(blank=True, max_length=100, null=True)),
                ('state', models.CharField(blank=True, max_length=100, null=True)),
                ('creation_time', models.DateTimeField(blank=True, null=True)),
                ('raw_data', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('ts', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'ebay_order_returns',
            },
        ),
    ]
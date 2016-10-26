# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2016-10-19 17:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rfi_sources', '0007_delete_amazonitemcachedhtmlpage'),
    ]

    operations = [
        migrations.CreateModel(
            name='AmazonItemDescription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asin', models.CharField(db_index=True, max_length=32)),
                ('parent_asin', models.CharField(blank=True, db_index=True, max_length=32, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('ts', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'amazon_item_descriptions',
            },
        ),
        migrations.CreateModel(
            name='AmazonItemFeature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asin', models.CharField(db_index=True, max_length=32)),
                ('parent_asin', models.CharField(blank=True, db_index=True, max_length=32, null=True)),
                ('features', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('ts', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'amazon_item_features',
            },
        ),
        migrations.CreateModel(
            name='AmazonItemMarketPrice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asin', models.CharField(db_index=True, max_length=32)),
                ('parent_asin', models.CharField(blank=True, db_index=True, max_length=32, null=True)),
                ('market_price', models.DecimalField(decimal_places=2, max_digits=15)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('ts', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'amazon_item_market_prices',
            },
        ),
        migrations.CreateModel(
            name='AmazonItemPrice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asin', models.CharField(db_index=True, max_length=32)),
                ('parent_asin', models.CharField(blank=True, db_index=True, max_length=32, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=15)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('ts', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'amazon_item_prices',
            },
        ),
        migrations.CreateModel(
            name='AmazonItemQuantity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asin', models.CharField(db_index=True, max_length=32)),
                ('parent_asin', models.CharField(blank=True, db_index=True, max_length=32, null=True)),
                ('quantity', models.SmallIntegerField(blank=True, default=0, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('ts', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'amazon_item_quantites',
            },
        ),
        migrations.CreateModel(
            name='AmazonItemTitle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asin', models.CharField(db_index=True, max_length=32)),
                ('parent_asin', models.CharField(blank=True, db_index=True, max_length=32, null=True)),
                ('title', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('ts', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'amazon_item_titles',
            },
        ),
    ]
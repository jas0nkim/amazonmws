# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2016-11-04 19:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rfi_account_profiles', '0004_auto_20160908_1543'),
    ]

    operations = [
        migrations.AddField(
            model_name='ebaystore',
            name='policy_shipping_international',
            field=models.TextField(blank=True, null=True),
        ),
    ]

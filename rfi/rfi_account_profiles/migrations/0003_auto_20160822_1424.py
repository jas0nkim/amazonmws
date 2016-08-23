# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-08-22 14:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rfi_account_profiles', '0002_ebaystore_margin_min_dollar'),
    ]

    operations = [
        migrations.AddField(
            model_name='amazonaccount',
            name='creditcard_number',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='amazonaccount',
            name='status',
            field=models.BooleanField(default=1),
        ),
    ]
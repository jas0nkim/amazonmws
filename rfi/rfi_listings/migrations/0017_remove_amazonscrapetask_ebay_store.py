# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-05-17 17:15
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rfi_listings', '0016_auto_20161205_1743'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='amazonscrapetask',
            name='ebay_store',
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-09-13 15:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rfi_sources', '0003_auto_20160603_1624'),
    ]

    operations = [
        migrations.AddField(
            model_name='amazonitem',
            name='parent_asin',
            field=models.CharField(blank=True, db_index=True, max_length=32, null=True),
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2016-12-02 19:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rfi_listings', '0014_auto_20161026_1900'),
    ]

    operations = [
        migrations.AddField(
            model_name='ebaystorecategory',
            name='level',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
    ]
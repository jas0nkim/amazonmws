# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-21 15:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rfi_orders', '0011_ebayorderreturn'),
    ]

    operations = [
        migrations.AddField(
            model_name='ebayorderreturn',
            name='comments',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2016-12-05 17:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rfi_listings', '0015_ebaystorecategory_level'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ebaystorecategory',
            name='name',
            field=models.CharField(db_index=True, max_length=100),
        ),
    ]
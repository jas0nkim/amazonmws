# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-11-06 22:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rfi_listings', '0023_archivedebayitem_archivedebayitemvariation'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='exclbrand',
            options={'verbose_name': 'Excluded Brand'},
        ),
        migrations.AddField(
            model_name='ebayitemstat',
            name='reason_hide_from_search',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
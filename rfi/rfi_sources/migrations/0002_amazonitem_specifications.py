# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-01 15:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rfi_sources', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='amazonitem',
            name='specifications',
            field=models.TextField(blank=True, null=True),
        ),
    ]

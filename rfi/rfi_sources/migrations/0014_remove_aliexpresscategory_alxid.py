# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-19 20:02
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rfi_sources', '0013_aliexpressstore'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='aliexpresscategory',
            name='alxid',
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-04-17 13:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ks_crm', '0004_auto_20180411_1253'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actions',
            name='end_time',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='actions',
            name='start_time',
            field=models.DateField(),
        ),
    ]

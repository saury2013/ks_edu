# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-04-19 14:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ks_crm', '0009_auto_20180419_2255'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='icon',
            field=models.CharField(default='fa-flask', max_length=32),
        ),
    ]
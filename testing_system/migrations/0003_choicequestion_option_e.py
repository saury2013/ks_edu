# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-04-08 07:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testing_system', '0002_auto_20180408_1527'),
    ]

    operations = [
        migrations.AddField(
            model_name='choicequestion',
            name='option_e',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
    ]
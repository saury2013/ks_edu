# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-04-11 04:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ks_crm', '0003_auto_20180411_1128'),
    ]

    operations = [
        migrations.AddField(
            model_name='actions',
            name='enabled',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='course',
            name='enabled',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='news',
            name='enabled',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='teachermaterials',
            name='enabled',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='actions',
            name='image',
            field=models.FileField(upload_to='action_image'),
        ),
        migrations.AlterField(
            model_name='news',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='news_image'),
        ),
    ]

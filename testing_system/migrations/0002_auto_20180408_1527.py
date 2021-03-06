# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-04-08 07:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testing_system', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='writingtask',
            options={'verbose_name': '写作题', 'verbose_name_plural': '写作题'},
        ),
        migrations.RemoveField(
            model_name='paperstruct',
            name='question_index',
        ),
        migrations.AddField(
            model_name='choicequestion',
            name='question_index',
            field=models.SmallIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='essayquestion',
            name='question_index',
            field=models.SmallIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='gapfilling',
            name='question_index',
            field=models.SmallIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='paperstruct',
            name='ps_index',
            field=models.SmallIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='writingtask',
            name='question_index',
            field=models.SmallIntegerField(default=1),
        ),
    ]

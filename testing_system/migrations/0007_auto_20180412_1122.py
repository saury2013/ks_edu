# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-04-12 03:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('testing_system', '0006_auto_20180410_2111'),
    ]

    operations = [
        migrations.CreateModel(
            name='StuAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ps_index', models.SmallIntegerField()),
                ('question_index', models.SmallIntegerField()),
                ('answer', models.TextField()),
                ('score', models.IntegerField()),
            ],
            options={
                'verbose_name': '答题卡',
                'verbose_name_plural': '答题卡',
            },
        ),
        migrations.AlterModelOptions(
            name='answerpaper',
            options={'verbose_name': '测试结果', 'verbose_name_plural': '测试结果'},
        ),
        migrations.RenameField(
            model_name='answerpaper',
            old_name='stu_id',
            new_name='student',
        ),
        migrations.RenameField(
            model_name='answerpaper',
            old_name='paper_id',
            new_name='test_paper',
        ),
        migrations.RemoveField(
            model_name='answerpaper',
            name='ps_index',
        ),
        migrations.RemoveField(
            model_name='answerpaper',
            name='question_index',
        ),
        migrations.RemoveField(
            model_name='answerpaper',
            name='stu_answer',
        ),
        migrations.AddField(
            model_name='stuanswer',
            name='answer_paper',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='testing_system.AnswerPaper'),
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-25 09:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0010_auto_20171222_2058'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='date',
            field=models.DateTimeField(default='1999-01-01 01:01:01'),
        ),
    ]

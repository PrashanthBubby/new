# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-22 15:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0009_auto_20171222_2013'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comments',
            old_name='commenter',
            new_name='commenter_id',
        ),
        migrations.AddField(
            model_name='comments',
            name='commenter_name',
            field=models.CharField(default='name', max_length=150),
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-27 18:51
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0014_auto_20171227_2005'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='likes',
            name='liked_post_title',
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-23 14:04
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0024_monthboard_weekboard'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='monthboard',
            name='leaderboard_ptr',
        ),
        migrations.RemoveField(
            model_name='weekboard',
            name='leaderboard_ptr',
        ),
        migrations.DeleteModel(
            name='MonthBoard',
        ),
        migrations.DeleteModel(
            name='WeekBoard',
        ),
    ]

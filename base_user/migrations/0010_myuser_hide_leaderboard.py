# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-28 09:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base_user', '0009_myuser_social_share_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='hide_leaderboard',
            field=models.BooleanField(default=False, help_text='Bu istifadəçi Liderborda düşmür'),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-11 16:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0016_auto_20170911_2006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='websiteheader',
            name='sub_text',
            field=models.TextField(blank=True, null=True),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-11 16:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0015_websiteheader'),
    ]

    operations = [
        migrations.AlterField(
            model_name='websiteheader',
            name='sub_text',
            field=models.TextField(default='Lorem ipsum dolor sit amet, consectetur adipisicing elit'),
        ),
    ]

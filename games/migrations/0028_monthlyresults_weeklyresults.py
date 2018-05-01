# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-29 20:04
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0027_auto_20170929_0026'),
    ]

    operations = [
        migrations.CreateModel(
            name='MonthlyResults',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('start', models.DateField()),
                ('end', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='WeeklyResults',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('start', models.DateField()),
                ('end', models.DateField()),
            ],
        ),
    ]
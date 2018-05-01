# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-11 15:51
from __future__ import unicode_literals

from django.db import migrations, models
from django.utils import timezone


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0014_auto_20170816_1807'),
    ]

    operations = [
        migrations.CreateModel(
            name='WebsiteHeader',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='25 İLLİK FƏALİYYƏT, BİR ƏSRLİK NƏAİYYƏT', max_length=255)),
                ('sub_text', models.TimeField(default=timezone.now)),
                ('facebook_link', models.URLField(blank=True, null=True)),
                ('twitter_link', models.URLField(blank=True, null=True)),
                ('instagram_link', models.URLField(blank=True, null=True)),
                ('youtube_link', models.URLField(blank=True, null=True)),
            ],
        ),
    ]

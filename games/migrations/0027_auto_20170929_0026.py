# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-28 20:26
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('games', '0026_monthboard_weekboard'),
    ]

    operations = [
        migrations.AddField(
            model_name='leaderboard',
            name='duration',
            field=models.DurationField(default=datetime.timedelta(0)),
        ),
        migrations.AddField(
            model_name='leaderboard',
            name='player',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='leaderboard',
            name='score',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='monthboard',
            name='duration',
            field=models.DurationField(default=datetime.timedelta(0)),
        ),
        migrations.AddField(
            model_name='monthboard',
            name='player',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='monthboard',
            name='score',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='weekboard',
            name='duration',
            field=models.DurationField(default=datetime.timedelta(0)),
        ),
        migrations.AddField(
            model_name='weekboard',
            name='player',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='weekboard',
            name='score',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='leaderboard',
            name='games',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='games.GameTime'),
        ),
        migrations.AlterField(
            model_name='monthboard',
            name='games',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='games.GameTime'),
        ),
        migrations.AlterField(
            model_name='weekboard',
            name='games',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='games.GameTime'),
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-06-15 12:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('summer_plans', '0016_lottery_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar_color',
            field=models.IntegerField(choices=[(1, '#A0C1E5'), (2, '#506B90'), (3, '#E5A1A0'), (4, '#D6A0E5'), (5, '#DAE5A0')], default=1),
        ),
    ]

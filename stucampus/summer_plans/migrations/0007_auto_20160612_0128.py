# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-06-11 17:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('summer_plans', '0006_auto_20160611_1623'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plan',
            name='content',
            field=models.TextField(max_length=1000, verbose_name='\u5185\u5bb9'),
        ),
    ]
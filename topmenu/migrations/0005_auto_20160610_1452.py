# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-10 21:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('topmenu', '0004_auto_20160608_0830'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone_num',
            field=models.BigIntegerField(max_length=10),
        ),
    ]

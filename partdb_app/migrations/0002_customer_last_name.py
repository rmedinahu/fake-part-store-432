# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-14 20:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partdb_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='last_name',
            field=models.CharField(default='', max_length=128),
            preserve_default=False,
        ),
    ]

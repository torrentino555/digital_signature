# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-07 01:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base_model', '0014_meeting'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='Invoice',
        ),
        migrations.AlterField(
            model_name='order',
            name='Text',
            field=models.TextField(default='', max_length=500),
        ),
    ]

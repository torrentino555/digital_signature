# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-24 23:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base_model', '0004_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='admin',
            field=models.BooleanField(default=False),
        ),
    ]
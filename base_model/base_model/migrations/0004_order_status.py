# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-20 21:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base_model', '0003_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='Status',
            field=models.CharField(default='\u0412 \u0440\u0430\u0441\u0441\u043c\u043e\u0442\u0440\u0435\u043d\u0438\u0438', max_length=30),
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-08-03 00:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base_model', '0008_auto_20170803_0231'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='Invoice',
            field=models.FileField(default=b'/home/log.log', null=True, upload_to=b''),
        ),
    ]

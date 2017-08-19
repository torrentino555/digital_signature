# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-08-05 17:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base_model', '0010_auto_20170805_2031'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Isp', models.BooleanField()),
                ('Token', models.BooleanField()),
                ('Help', models.BooleanField()),
                ('Date', models.DateField()),
                ('Status', models.CharField(default='\u0412 \u0440\u0430\u0441\u0441\u043c\u043e\u0442\u0440\u0435\u043d\u0438\u0438', max_length=30)),
                ('Number', models.IntegerField(default=0)),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base_model.Person')),
            ],
        ),
    ]

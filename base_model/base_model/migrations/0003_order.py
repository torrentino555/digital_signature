# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-15 18:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base_model', '0002_person_user'),
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
                ('Number', models.IntegerField(default=0)),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base_model.Person')),
            ],
        ),
    ]

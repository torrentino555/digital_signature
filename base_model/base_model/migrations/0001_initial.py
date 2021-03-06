# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-14 13:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Surname', models.CharField(max_length=50)),
                ('Firstname', models.CharField(max_length=50)),
                ('GivenName', models.CharField(max_length=50)),
                ('Country', models.CharField(max_length=50)),
                ('State', models.CharField(max_length=50)),
                ('Locality', models.CharField(max_length=50)),
                ('StreetAddress', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=50)),
                ('INN', models.CharField(max_length=12)),
                ('SNILS', models.CharField(max_length=11)),
            ],
        ),
    ]

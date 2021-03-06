# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-30 21:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TrendRegister',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('TimeStamp', models.DateTimeField()),
                ('Temp1', models.FloatField()),
                ('Temp2', models.FloatField()),
                ('Temp3', models.FloatField()),
                ('Temp4', models.FloatField()),
                ('HotFlow', models.FloatField()),
                ('ColdFlow', models.FloatField()),
                ('PumpSpeed', models.FloatField()),
            ],
            options={
                'ordering': ['TimeStamp'],
                'verbose_name_plural': 'TrendRegisters',
                'verbose_name': 'TrendRegister',
            },
        ),
    ]

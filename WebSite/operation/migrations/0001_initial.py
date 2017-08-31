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
            name='DataDisplay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='Nome')),
                ('UE', models.CharField(blank=True, max_length=10, null=True, verbose_name='UE')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Descrição Simples')),
                ('Tag', models.CharField(blank=True, max_length=10, null=True, verbose_name='Tag')),
                ('Value', models.FloatField(verbose_name='Valor')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name_plural': 'Displays',
                'verbose_name': 'Display',
            },
        ),
        migrations.CreateModel(
            name='OperationMode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('OpMode', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Registers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('TimeStamp', models.DateTimeField()),
                ('Temp1', models.FloatField()),
                ('Temp2', models.FloatField()),
                ('Temp3', models.FloatField()),
                ('Temp4', models.FloatField()),
                ('HotFlow', models.FloatField()),
                ('ColdFlow', models.FloatField()),
                ('PumpStatus', models.BooleanField()),
                ('HeaterStatus', models.BooleanField()),
                ('ArduinoMode', models.BooleanField()),
                ('PumpSpeed', models.FloatField()),
            ],
            options={
                'ordering': ['TimeStamp'],
                'verbose_name_plural': 'Registers',
                'verbose_name': 'Register',
            },
        ),
    ]

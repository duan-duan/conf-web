# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-06-11 18:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Confd',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(max_length=40, verbose_name='\u9879\u76ee\u540d\u79f0')),
                ('server_name', models.CharField(max_length=40, verbose_name='\u57df\u540d')),
                ('server_root', models.CharField(max_length=40, verbose_name='\u7a0b\u5e8f\u76ee\u5f55')),
            ],
        ),
    ]

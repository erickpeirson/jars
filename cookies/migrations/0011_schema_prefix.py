# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-09-09 18:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cookies', '0010_auto_20160729_1804'),
    ]

    operations = [
        migrations.AddField(
            model_name='schema',
            name='prefix',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
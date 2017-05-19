# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-05-19 14:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cookies', '0012_datasetsnapshot'),
    ]

    operations = [
        migrations.AddField(
            model_name='datasetsnapshot',
            name='state',
            field=models.CharField(choices=[(b'PE', b'Pending'), (b'IP', b'In progress'), (b'DO', b'Done'), (b'ER', b'Error')], default=b'PE', max_length=2),
        ),
    ]

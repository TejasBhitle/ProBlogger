# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-09-15 04:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_post_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='height',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='width',
            field=models.IntegerField(default=0, null=True),
        ),
    ]

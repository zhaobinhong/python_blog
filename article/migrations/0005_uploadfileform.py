# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-25 05:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0004_auto_20170405_0541'),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadFileForm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('file', models.FileField(upload_to=b'')),
            ],
        ),
    ]

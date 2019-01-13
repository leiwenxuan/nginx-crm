# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-11-28 21:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpurview',
            name='menu',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rbac.menu', verbose_name='所属菜单'),
        ),
        migrations.AlterField(
            model_name='userpurview',
            name='name',
            field=models.CharField(max_length=24, unique=True, verbose_name='路由别名'),
        ),
    ]

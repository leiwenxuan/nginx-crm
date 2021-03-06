# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-12-01 13:35
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0004_auto_20181130_1443'),
    ]

    operations = [
        migrations.AlterField(
            model_name='role',
            name='user',
            field=models.ManyToManyField(null=True, related_name='roles', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='userpurview',
            name='menu',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rbac.Menu', verbose_name='所属菜单'),
        ),
    ]

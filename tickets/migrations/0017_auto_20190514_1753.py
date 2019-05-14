# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-05-14 17:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0016_auto_20190514_1749'),
    ]

    operations = [
        migrations.AddField(
            model_name='show',
            name='warnings_action',
            field=models.ManyToManyField(blank=True, related_name='warnings_action', to='tickets.ContentWarning'),
        ),
        migrations.AddField(
            model_name='show',
            name='warnings_dialogue',
            field=models.ManyToManyField(blank=True, related_name='warnings_dialogue', to='tickets.ContentWarning'),
        ),
        migrations.AlterField(
            model_name='show',
            name='warnings_technical',
            field=models.ManyToManyField(blank=True, related_name='warnings_technical', to='tickets.ContentWarning'),
        ),
    ]
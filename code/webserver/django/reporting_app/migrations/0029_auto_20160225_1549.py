# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reporting_app', '0028_eventcounter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fault',
            name='alarm_condition',
            field=models.CharField(default='unknown', max_length=256, serialize=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='fault',
            name='event_type',
            field=models.CharField(default='unknown', max_length=64, blank=True),
        ),
        migrations.AlterField(
            model_name='fault',
            name='specific_problem',
            field=models.CharField(default='unknown', max_length=256),
        ),
    ]

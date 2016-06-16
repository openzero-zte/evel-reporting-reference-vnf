# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reporting_app', '0030_auto_20160225_1550'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fault',
            name='alarm_condition',
            field=models.CharField(max_length=256, serialize=False, primary_key=True),
        ),
    ]

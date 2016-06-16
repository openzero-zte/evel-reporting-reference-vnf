# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reporting_app', '0016_auto_20160217_1552'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mobileflow',
            name='dur_connection_failed_status',
            field=models.FloatField(default=0, null=True),
        ),
    ]

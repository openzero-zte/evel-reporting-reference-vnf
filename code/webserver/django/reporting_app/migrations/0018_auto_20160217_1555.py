# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reporting_app', '0017_auto_20160217_1554'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mobileflow',
            name='dur_connection_failed_status',
            field=models.FloatField(default=0, blank=True),
        ),
    ]

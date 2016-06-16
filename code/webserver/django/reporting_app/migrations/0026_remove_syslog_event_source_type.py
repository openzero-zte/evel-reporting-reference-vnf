# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reporting_app', '0025_auto_20160223_1342'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='syslog',
            name='event_source_type',
        ),
    ]

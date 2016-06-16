# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reporting_app', '0026_remove_syslog_event_source_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='syslog',
            name='syslog_fields_version',
        ),
    ]

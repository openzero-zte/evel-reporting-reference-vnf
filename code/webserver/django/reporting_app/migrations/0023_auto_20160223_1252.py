# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reporting_app', '0022_syslog'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='syslog',
            name='syslog_fields_version',
        ),
        migrations.RemoveField(
            model_name='syslog',
            name='syslog_proc_id',
        ),
        migrations.RemoveField(
            model_name='syslog',
            name='syslog_ver',
        ),
    ]

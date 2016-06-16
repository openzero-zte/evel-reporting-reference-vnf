# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reporting_app', '0021_auto_20160218_0838'),
    ]

    operations = [
        migrations.CreateModel(
            name='Syslog',
            fields=[
                ('friendly_name', models.CharField(max_length=64, serialize=False, primary_key=True)),
                ('event_type', models.CharField(max_length=64, blank=True)),
                ('syslog_fields_version', models.IntegerField(default=0)),
                ('syslog_proc_id', models.IntegerField(default=0)),
                ('syslog_ver', models.FloatField(default=0)),
            ],
            options={
                'ordering': ['friendly_name'],
            },
        ),
    ]

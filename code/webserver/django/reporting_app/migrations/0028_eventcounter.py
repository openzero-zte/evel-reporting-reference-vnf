# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reporting_app', '0027_remove_syslog_syslog_fields_version'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventCounter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('event_type', models.CharField(default=None, max_length=64)),
                ('count', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name': 'event counts',
                'verbose_name_plural': 'event counts',
            },
        ),
    ]

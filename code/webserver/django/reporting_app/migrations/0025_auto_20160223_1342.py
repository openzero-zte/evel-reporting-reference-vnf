# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reporting_app', '0024_auto_20160223_1256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mobileflow',
            name='flow_deactivation_time',
            field=models.CharField(default='unknown', max_length=64, blank=True),
        ),
        migrations.AlterField(
            model_name='mobileflow',
            name='flow_direction',
            field=models.CharField(default='unknown', max_length=64, blank=True),
        ),
        migrations.AlterField(
            model_name='mobileflow',
            name='ip_protocol_type',
            field=models.CharField(default='unknown', max_length=64, blank=True),
        ),
        migrations.AlterField(
            model_name='mobileflow',
            name='ip_version',
            field=models.CharField(default='unknown', max_length=64, blank=True),
        ),
        migrations.AlterField(
            model_name='mobileflow',
            name='other_endpoint_ip_address',
            field=models.CharField(default='unknown', max_length=64, blank=True),
        ),
        migrations.AlterField(
            model_name='mobileflow',
            name='reporting_endpoint_ip_addr',
            field=models.CharField(default='unknown', max_length=64, blank=True),
        ),
        migrations.AlterField(
            model_name='syslog',
            name='syslog_msg',
            field=models.CharField(default='unknown', max_length=256, blank=True),
        ),
        migrations.AlterField(
            model_name='syslog',
            name='syslog_tag',
            field=models.CharField(default='unknown', max_length=256, blank=True),
        ),
    ]

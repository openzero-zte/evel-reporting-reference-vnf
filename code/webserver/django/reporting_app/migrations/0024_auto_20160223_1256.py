# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reporting_app', '0023_auto_20160223_1252'),
    ]

    operations = [
        migrations.AddField(
            model_name='syslog',
            name='event_source_host',
            field=models.CharField(max_length=256, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='syslog',
            name='event_source_type',
            field=models.CharField(default=b'OTHER', max_length=16, choices=[(b'OTHER', b'other(0)'), (b'ROUTER', b'router(1)'), (b'SWITCH', b'switch(2)'), (b'HOST', b'host(3)'), (b'CARD', b'card(4)'), (b'PORT', b'port(5)'), (b'SLOT_THRESHOLD', b'slotThreshold(6)'), (b'PORT_THRESHOLD', b'portThreshold(7)'), (b'VIRTUAL_MACHINE', b'virtualMachine(8)'), (b'VIRTUAL_NETWORK_FUNCTION', b'virtualNetworkFunction(9)')]),
        ),
        migrations.AddField(
            model_name='syslog',
            name='syslog_facility',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='syslog',
            name='syslog_fields_version',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='syslog',
            name='syslog_msg',
            field=models.CharField(default='unkown', max_length=256, blank=True),
        ),
        migrations.AddField(
            model_name='syslog',
            name='syslog_proc',
            field=models.CharField(max_length=256, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='syslog',
            name='syslog_proc_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='syslog',
            name='syslog_sdata',
            field=models.CharField(max_length=256, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='syslog',
            name='syslog_tag',
            field=models.CharField(default='unkown', max_length=256, blank=True),
        ),
        migrations.AddField(
            model_name='syslog',
            name='syslog_ver',
            field=models.FloatField(default=0),
        ),
    ]

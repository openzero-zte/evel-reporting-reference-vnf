# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reporting_app', '0002_remove_measurement_severity'),
    ]

    operations = [
        migrations.CreateModel(
            name='GtpPerFlowMetrics',
            fields=[
                ('friendly_name', models.CharField(max_length=64, serialize=False, primary_key=True)),
                ('avg_bit_error_rate', models.FloatField(default=0)),
                ('avg_packet_delay_variation', models.FloatField(default=0)),
                ('avg_packet_latency', models.FloatField(default=0)),
                ('avg_receive_throughput', models.FloatField(default=0)),
            ],
            options={
                'ordering': ['friendly_name'],
            },
        ),
    ]

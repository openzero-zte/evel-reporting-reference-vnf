# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Fault',
            fields=[
                ('event_type', models.CharField(max_length=64, blank=True)),
                ('severity', models.CharField(max_length=16, choices=[(b'CRITICAL', b'Critical'), (b'MAJOR', b'Major'), (b'MINOR', b'Minor'), (b'WARNING', b'Warning'), (b'NORMAL', b'Normal')])),
                ('alarm_condition', models.CharField(max_length=256, serialize=False, primary_key=True)),
                ('specific_problem', models.CharField(max_length=256)),
                ('alarm_a_interface', models.CharField(max_length=64, blank=True)),
            ],
            options={
                'ordering': ['alarm_condition'],
            },
        ),
        migrations.CreateModel(
            name='FaultAdditionalInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('value', models.CharField(max_length=64)),
                ('fault', models.ForeignKey(to='reporting_app.Fault')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Measurement',
            fields=[
                ('measurement_name', models.CharField(max_length=64, serialize=False, primary_key=True)),
                ('event_type', models.CharField(max_length=64, blank=True)),
                ('severity', models.CharField(max_length=16, choices=[(b'CRITICAL', b'Critical'), (b'MAJOR', b'Major'), (b'MINOR', b'Minor'), (b'WARNING', b'Warning'), (b'NORMAL', b'Normal')])),
                ('aggregate_cpu_usage', models.FloatField(default=0)),
                ('concurrent_sessions', models.IntegerField(default=0)),
                ('configured_entities', models.IntegerField(default=0)),
                ('mean_request_latency', models.FloatField(default=0)),
                ('measurement_interval', models.FloatField(default=0)),
                ('memory_configured', models.FloatField(default=0)),
                ('memory_used', models.FloatField(default=0)),
                ('media_ports_in_use', models.IntegerField(default=0)),
                ('request_rate', models.IntegerField(default=0)),
                ('scaling_metric', models.FloatField(default=0)),
            ],
            options={
                'ordering': ['measurement_name'],
            },
        ),
        migrations.CreateModel(
            name='MeasurementAdditionalMeasurementGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('name_1', models.CharField(max_length=64, blank=True)),
                ('value_1', models.CharField(max_length=64, blank=True)),
                ('name_2', models.CharField(max_length=64, blank=True)),
                ('value_2', models.CharField(max_length=64, blank=True)),
                ('name_3', models.CharField(max_length=64, blank=True)),
                ('value_3', models.CharField(max_length=64, blank=True)),
                ('name_4', models.CharField(max_length=64, blank=True)),
                ('value_4', models.CharField(max_length=64, blank=True)),
                ('measurement', models.ForeignKey(to='reporting_app.Measurement')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='MeasurementCodecInUse',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('identifier', models.CharField(max_length=64)),
                ('utilization', models.IntegerField(default=0)),
                ('measurement', models.ForeignKey(to='reporting_app.Measurement')),
            ],
            options={
                'ordering': ['identifier'],
            },
        ),
        migrations.CreateModel(
            name='MeasurementCPUUse',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('identifier', models.CharField(max_length=64)),
                ('utilization', models.IntegerField(default=0)),
                ('measurement', models.ForeignKey(to='reporting_app.Measurement')),
            ],
            options={
                'ordering': ['identifier'],
            },
        ),
        migrations.CreateModel(
            name='MeasurementFeatureInUse',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('identifier', models.CharField(max_length=64)),
                ('utilization', models.IntegerField(default=0)),
                ('measurement', models.ForeignKey(to='reporting_app.Measurement')),
            ],
            options={
                'ordering': ['identifier'],
            },
        ),
        migrations.CreateModel(
            name='MeasurementFileSystemUse',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('identifier', models.UUIDField()),
                ('block_configured', models.IntegerField(default=0)),
                ('block_iops', models.IntegerField(default=0)),
                ('block_used', models.IntegerField(default=0)),
                ('ephemeral_configured', models.IntegerField(default=0)),
                ('ephemeral_iops', models.IntegerField(default=0)),
                ('ephemeral_used', models.IntegerField(default=0)),
                ('measurement', models.ForeignKey(to='reporting_app.Measurement')),
            ],
            options={
                'ordering': ['identifier'],
            },
        ),
        migrations.CreateModel(
            name='MeasurementLatencyDistribution',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('low_end', models.FloatField(default=0)),
                ('high_end', models.FloatField(default=0)),
                ('count', models.IntegerField(default=0)),
                ('measurement', models.ForeignKey(to='reporting_app.Measurement')),
            ],
            options={
                'ordering': ['low_end'],
            },
        ),
        migrations.CreateModel(
            name='MeasurementVNICUse',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('identifier', models.CharField(max_length=64)),
                ('broadcast_packets_in', models.IntegerField(default=0)),
                ('broadcast_packets_out', models.IntegerField(default=0)),
                ('bytes_in', models.IntegerField(default=0)),
                ('bytes_out', models.IntegerField(default=0)),
                ('multicast_packets_in', models.IntegerField(default=0)),
                ('multicast_packets_out', models.IntegerField(default=0)),
                ('unicast_packets_in', models.IntegerField(default=0)),
                ('unicast_packets_out', models.IntegerField(default=0)),
                ('measurement', models.ForeignKey(to='reporting_app.Measurement')),
            ],
            options={
                'ordering': ['identifier'],
            },
        ),
        migrations.CreateModel(
            name='ReportingAppConfig',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('collector_url', models.URLField()),
                ('topology', models.CharField(max_length=20, choices=[(b'SINGLETON', b'Singleton'), (b'HA-PAIR', b'HA Pair'), (b'CLUSTER', b'Cluster')])),
            ],
            options={
                'verbose_name': 'event reporting application configuration',
                'verbose_name_plural': 'event reporting application configuration',
            },
        ),
    ]

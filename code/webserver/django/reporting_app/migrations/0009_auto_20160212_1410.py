# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reporting_app', '0008_gtpmobileqcicoscount_gtptcpflagcount'),
    ]

    operations = [
        migrations.CreateModel(
            name='GtpMetricIpTos',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.CharField(max_length=64)),
                ('gtp_per_flow_metrics', models.ForeignKey(to='reporting_app.GtpPerFlowMetrics')),
            ],
            options={
                'ordering': ['value'],
            },
        ),
        migrations.CreateModel(
            name='GtpMetricMobileQciCos',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.CharField(max_length=64)),
                ('gtp_per_flow_metrics', models.ForeignKey(to='reporting_app.GtpPerFlowMetrics')),
            ],
            options={
                'ordering': ['value'],
            },
        ),
        migrations.CreateModel(
            name='GtpMetricMobileQciCosCount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(max_length=64)),
                ('value', models.CharField(max_length=64)),
                ('gtp_per_flow_metrics', models.ForeignKey(to='reporting_app.GtpPerFlowMetrics')),
            ],
            options={
                'ordering': ['key'],
            },
        ),
        migrations.CreateModel(
            name='GtpMetricTcpFlag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.CharField(max_length=64)),
                ('gtp_per_flow_metrics', models.ForeignKey(to='reporting_app.GtpPerFlowMetrics')),
            ],
            options={
                'ordering': ['value'],
            },
        ),
        migrations.CreateModel(
            name='GtpMetricTcpFlagCount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(max_length=64)),
                ('value', models.CharField(max_length=64)),
                ('gtp_per_flow_metrics', models.ForeignKey(to='reporting_app.GtpPerFlowMetrics')),
            ],
            options={
                'ordering': ['key'],
            },
        ),
        migrations.RemoveField(
            model_name='gtpmobileqcicoscount',
            name='gtp_per_flow_metrics',
        ),
        migrations.RemoveField(
            model_name='gtptcpflagcount',
            name='gtp_per_flow_metrics',
        ),
        migrations.DeleteModel(
            name='GtpMobileQciCosCount',
        ),
        migrations.DeleteModel(
            name='GtpTcpFlagCount',
        ),
    ]

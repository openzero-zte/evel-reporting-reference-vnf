# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reporting_app', '0007_auto_20160212_1154'),
    ]

    operations = [
        migrations.CreateModel(
            name='GtpMobileQciCosCount',
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
            name='GtpTcpFlagCount',
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
    ]

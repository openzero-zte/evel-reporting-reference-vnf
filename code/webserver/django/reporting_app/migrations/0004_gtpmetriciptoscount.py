# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reporting_app', '0003_gtpperflowmetrics'),
    ]

    operations = [
        migrations.CreateModel(
            name='GtpMetricIpTosCount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.IntegerField(default=0)),
                ('utilization', models.IntegerField(default=0)),
                ('gtp_per_flow_metrics', models.ForeignKey(to='reporting_app.GtpPerFlowMetrics')),
            ],
            options={
                'ordering': ['key'],
            },
        ),
    ]

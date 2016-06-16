# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reporting_app', '0006_auto_20160212_1004'),
    ]

    operations = [
        migrations.AddField(
            model_name='gtpperflowmetrics',
            name='durConnectionFailedStatus',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='gtpperflowmetrics',
            name='durTunnelFailedStatus',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='gtpperflowmetrics',
            name='flowActivatedBy',
            field=models.CharField(max_length=64, blank=True),
        ),
        migrations.AddField(
            model_name='gtpperflowmetrics',
            name='flowActivationTime',
            field=models.CharField(max_length=64, blank=True),
        ),
        migrations.AddField(
            model_name='gtpperflowmetrics',
            name='flowDeactivatedBy',
            field=models.CharField(max_length=64, blank=True),
        ),
        migrations.AddField(
            model_name='gtpperflowmetrics',
            name='gtpConnectionStatus',
            field=models.CharField(max_length=64, blank=True),
        ),
        migrations.AddField(
            model_name='gtpperflowmetrics',
            name='gtpTunnelStatus',
            field=models.CharField(max_length=64, blank=True),
        ),
        migrations.AddField(
            model_name='gtpperflowmetrics',
            name='largePacketRtt',
            field=models.FloatField(default=0, blank=True),
        ),
        migrations.AddField(
            model_name='gtpperflowmetrics',
            name='largePacketThreshold',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='gtpperflowmetrics',
            name='maxReceiveBitRate',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='gtpperflowmetrics',
            name='maxTransmitBitRate',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='gtpperflowmetrics',
            name='numGtpEchoFailures',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='gtpperflowmetrics',
            name='numGtpTunnelErrors',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='gtpperflowmetrics',
            name='numHttpErrors',
            field=models.IntegerField(default=0),
        ),
    ]

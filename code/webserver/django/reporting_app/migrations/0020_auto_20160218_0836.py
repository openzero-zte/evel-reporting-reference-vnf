# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reporting_app', '0019_auto_20160218_0833'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mobileflow',
            name='dur_connection_failed_status',
            field=models.FloatField(default=0, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='mobileflow',
            name='dur_tunnel_failed_status',
            field=models.FloatField(default=0, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='mobileflow',
            name='flow_activated_by',
            field=models.CharField(max_length=64, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='mobileflow',
            name='flow_activation_time',
            field=models.CharField(max_length=64, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='mobileflow',
            name='flow_deactivated_by',
            field=models.CharField(max_length=64, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='mobileflow',
            name='gtp_connection_status',
            field=models.CharField(max_length=64, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='mobileflow',
            name='gtp_tunnel_status',
            field=models.CharField(max_length=64, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='mobileflow',
            name='large_packet_rtt',
            field=models.FloatField(default=0, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='mobileflow',
            name='large_packet_threshold',
            field=models.IntegerField(default=0, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='mobileflow',
            name='max_receive_bit_rate',
            field=models.IntegerField(default=0, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='mobileflow',
            name='max_transmit_bit_rate',
            field=models.IntegerField(default=0, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='mobileflow',
            name='num_gtp_echo_failures',
            field=models.IntegerField(default=0, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='mobileflow',
            name='num_gtp_tunnel_errors',
            field=models.IntegerField(default=0, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='mobileflow',
            name='num_http_errors',
            field=models.IntegerField(default=0, null=True, blank=True),
        ),
    ]

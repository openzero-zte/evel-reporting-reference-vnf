# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reporting_app', '0009_auto_20160212_1410'),
    ]

    operations = [
        migrations.RenameField(
            model_name='gtpperflowmetrics',
            old_name='durConnectionFailedStatus',
            new_name='dur_connection_failed_status',
        ),
        migrations.RenameField(
            model_name='gtpperflowmetrics',
            old_name='durTunnelFailedStatus',
            new_name='dur_tunnel_failed_status',
        ),
        migrations.RenameField(
            model_name='gtpperflowmetrics',
            old_name='flowActivatedBy',
            new_name='flow_activated_by',
        ),
        migrations.RenameField(
            model_name='gtpperflowmetrics',
            old_name='flowActivationTime',
            new_name='flow_activation_time',
        ),
        migrations.RenameField(
            model_name='gtpperflowmetrics',
            old_name='flowDeactivatedBy',
            new_name='flow_deactivated_by',
        ),
        migrations.RenameField(
            model_name='gtpperflowmetrics',
            old_name='gtpConnectionStatus',
            new_name='gtp_connection_status',
        ),
        migrations.RenameField(
            model_name='gtpperflowmetrics',
            old_name='gtpTunnelStatus',
            new_name='gtp_tunnel_status',
        ),
        migrations.RenameField(
            model_name='gtpperflowmetrics',
            old_name='largePacketRtt',
            new_name='large_packet_rtt',
        ),
        migrations.RenameField(
            model_name='gtpperflowmetrics',
            old_name='largePacketThreshold',
            new_name='large_packet_threshold',
        ),
        migrations.RenameField(
            model_name='gtpperflowmetrics',
            old_name='maxReceiveBitRate',
            new_name='max_receive_bit_rate',
        ),
        migrations.RenameField(
            model_name='gtpperflowmetrics',
            old_name='maxTransmitBitRate',
            new_name='max_transmit_bit_rate',
        ),
        migrations.RenameField(
            model_name='gtpperflowmetrics',
            old_name='numGtpEchoFailures',
            new_name='num_gtp_echo_failures',
        ),
        migrations.RenameField(
            model_name='gtpperflowmetrics',
            old_name='numGtpTunnelErrors',
            new_name='num_gtp_tunnel_errors',
        ),
        migrations.RenameField(
            model_name='gtpperflowmetrics',
            old_name='numHttpErrors',
            new_name='num_http_errors',
        ),
    ]

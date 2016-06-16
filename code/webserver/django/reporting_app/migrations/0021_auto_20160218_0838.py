# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reporting_app', '0020_auto_20160218_0836'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mobileflow',
            name='dur_connection_failed_status',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='mobileflow',
            name='dur_tunnel_failed_status',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='mobileflow',
            name='large_packet_rtt',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='mobileflow',
            name='large_packet_threshold',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='mobileflow',
            name='max_receive_bit_rate',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='mobileflow',
            name='max_transmit_bit_rate',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='mobileflow',
            name='num_gtp_echo_failures',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='mobileflow',
            name='num_gtp_tunnel_errors',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='mobileflow',
            name='num_http_errors',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='mobileflow',
            name='sampling_algorithm',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]

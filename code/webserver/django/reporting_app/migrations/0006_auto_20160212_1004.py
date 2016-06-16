# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('reporting_app', '0005_auto_20160212_0756'),
    ]

    operations = [
        migrations.AddField(
            model_name='gtpperflowmetrics',
            name='avg_transmit_throughput',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='gtpperflowmetrics',
            name='flow_activation_epoch',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='gtpperflowmetrics',
            name='flow_activation_microsec',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='gtpperflowmetrics',
            name='flow_deactivation_epoch',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='gtpperflowmetrics',
            name='flow_deactivation_microsec',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='gtpperflowmetrics',
            name='flow_deactivation_time',
            field=models.CharField(default='unkown', max_length=64, blank=True),
        ),
        migrations.AddField(
            model_name='gtpperflowmetrics',
            name='flow_status',
            field=models.CharField(default=datetime.datetime(2016, 2, 12, 10, 4, 49, 42000, tzinfo=utc), max_length=20, choices=[(b'WORKING', b'working'), (b'INACTIVE', b'inactive'), (b'FAILED', b'failed')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='gtpperflowmetrics',
            name='max_packet_delay_variation',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='gtpperflowmetrics',
            name='num_L7_bytes_received',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='gtpperflowmetrics',
            name='num_L7_bytes_transmitted',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='gtpperflowmetrics',
            name='num_activation_failures',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='gtpperflowmetrics',
            name='num_bit_errors',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='gtpperflowmetrics',
            name='num_bytes_received',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='gtpperflowmetrics',
            name='num_bytes_transmitted',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='gtpperflowmetrics',
            name='num_dropped_packets',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='gtpperflowmetrics',
            name='num_lost_packets',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='gtpperflowmetrics',
            name='num_out_of_order_packets',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='gtpperflowmetrics',
            name='num_packet_errors',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='gtpperflowmetrics',
            name='num_packets_received_excl_retrans',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='gtpperflowmetrics',
            name='num_packets_received_incl_retrans',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='gtpperflowmetrics',
            name='num_packets_transmitted_incl_retrans',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='gtpperflowmetrics',
            name='num_retries',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='gtpperflowmetrics',
            name='num_timeouts',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='gtpperflowmetrics',
            name='num_tunneled_L7_bytes_received',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='gtpperflowmetrics',
            name='round_trip_time',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='gtpperflowmetrics',
            name='time_to_first_byte',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='gtpperflowmetrics',
            name='avg_packet_delay_variation',
            field=models.IntegerField(default=0),
        ),
    ]

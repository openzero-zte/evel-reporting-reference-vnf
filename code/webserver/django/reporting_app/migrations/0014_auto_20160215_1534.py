# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reporting_app', '0013_auto_20160215_1400'),
    ]

    operations = [
        migrations.AddField(
            model_name='mobileflow',
            name='app_protocol_type',
            field=models.CharField(max_length=64, blank=True),
        ),
        migrations.AddField(
            model_name='mobileflow',
            name='app_protocol_version',
            field=models.CharField(max_length=64, blank=True),
        ),
        migrations.AddField(
            model_name='mobileflow',
            name='application_type',
            field=models.CharField(max_length=64, blank=True),
        ),
        migrations.AddField(
            model_name='mobileflow',
            name='cid',
            field=models.CharField(max_length=64, blank=True),
        ),
        migrations.AddField(
            model_name='mobileflow',
            name='connection_type',
            field=models.CharField(max_length=64, blank=True),
        ),
        migrations.AddField(
            model_name='mobileflow',
            name='ecgi',
            field=models.CharField(max_length=64, blank=True),
        ),
        migrations.AddField(
            model_name='mobileflow',
            name='flow_direction',
            field=models.CharField(default='unkown', max_length=64, blank=True),
        ),
        migrations.AddField(
            model_name='mobileflow',
            name='gtp_protocol_type',
            field=models.CharField(max_length=64, blank=True),
        ),
        migrations.AddField(
            model_name='mobileflow',
            name='gtp_version',
            field=models.CharField(max_length=64, blank=True),
        ),
        migrations.AddField(
            model_name='mobileflow',
            name='http_header',
            field=models.CharField(max_length=64, blank=True),
        ),
        migrations.AddField(
            model_name='mobileflow',
            name='imei',
            field=models.CharField(max_length=64, blank=True),
        ),
        migrations.AddField(
            model_name='mobileflow',
            name='imsi',
            field=models.CharField(max_length=64, blank=True),
        ),
        migrations.AddField(
            model_name='mobileflow',
            name='ip_protocol_type',
            field=models.CharField(default='unkown', max_length=64, blank=True),
        ),
        migrations.AddField(
            model_name='mobileflow',
            name='ip_version',
            field=models.CharField(default='unkown', max_length=64, blank=True),
        ),
        migrations.AddField(
            model_name='mobileflow',
            name='lac',
            field=models.CharField(max_length=64, blank=True),
        ),
        migrations.AddField(
            model_name='mobileflow',
            name='mcc',
            field=models.CharField(max_length=64, blank=True),
        ),
        migrations.AddField(
            model_name='mobileflow',
            name='mnc',
            field=models.CharField(max_length=64, blank=True),
        ),
        migrations.AddField(
            model_name='mobileflow',
            name='msisdn',
            field=models.CharField(max_length=64, blank=True),
        ),
        migrations.AddField(
            model_name='mobileflow',
            name='other_endpoint_ip_address',
            field=models.CharField(default='unkown', max_length=64, blank=True),
        ),
        migrations.AddField(
            model_name='mobileflow',
            name='other_endpoint_port',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='mobileflow',
            name='other_functional_role',
            field=models.CharField(max_length=64, blank=True),
        ),
        migrations.AddField(
            model_name='mobileflow',
            name='rac',
            field=models.CharField(max_length=64, blank=True),
        ),
        migrations.AddField(
            model_name='mobileflow',
            name='radio_access_technology',
            field=models.CharField(max_length=64, blank=True),
        ),
        migrations.AddField(
            model_name='mobileflow',
            name='reporting_endpoint_ip_addr',
            field=models.CharField(default='unkown', max_length=64, blank=True),
        ),
        migrations.AddField(
            model_name='mobileflow',
            name='reporting_endpoint_port',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='mobileflow',
            name='sac',
            field=models.CharField(max_length=64, blank=True),
        ),
        migrations.AddField(
            model_name='mobileflow',
            name='sampling_algorithm',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='mobileflow',
            name='tac',
            field=models.CharField(max_length=64, blank=True),
        ),
        migrations.AddField(
            model_name='mobileflow',
            name='tunnel_id',
            field=models.CharField(max_length=64, blank=True),
        ),
        migrations.AddField(
            model_name='mobileflow',
            name='vlan_id',
            field=models.CharField(max_length=64, blank=True),
        ),
    ]

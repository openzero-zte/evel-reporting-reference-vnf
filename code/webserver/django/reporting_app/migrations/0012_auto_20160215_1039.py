# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reporting_app', '0011_auto_20160215_1004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gtpmetricmobileqcicoscount',
            name='value',
            field=models.CharField(max_length=64),
        ),
        migrations.AlterField(
            model_name='gtpmetrictcpflagcount',
            name='value',
            field=models.CharField(max_length=64),
        ),
    ]

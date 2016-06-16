# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reporting_app', '0010_auto_20160212_1545'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gtpmetricmobileqcicoscount',
            name='value',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='gtpmetrictcpflagcount',
            name='value',
            field=models.IntegerField(default=0),
        ),
    ]

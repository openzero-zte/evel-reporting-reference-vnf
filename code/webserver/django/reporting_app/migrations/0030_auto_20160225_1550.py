# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reporting_app', '0029_auto_20160225_1549'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fault',
            name='severity',
            field=models.CharField(default=b'Normal', max_length=16, choices=[(b'CRITICAL', b'Critical'), (b'MAJOR', b'Major'), (b'MINOR', b'Minor'), (b'WARNING', b'Warning'), (b'NORMAL', b'Normal')]),
        ),
    ]

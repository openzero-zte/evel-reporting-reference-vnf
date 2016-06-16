# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reporting_app', '0004_gtpmetriciptoscount'),
    ]

    operations = [
        migrations.RenameField(
            model_name='gtpmetriciptoscount',
            old_name='utilization',
            new_name='value',
        ),
    ]

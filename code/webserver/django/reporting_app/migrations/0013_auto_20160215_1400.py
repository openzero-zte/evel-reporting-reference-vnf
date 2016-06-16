# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reporting_app', '0012_auto_20160215_1039'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='GtpPerFlowMetrics',
            new_name='MobileFlow',
        ),
    ]

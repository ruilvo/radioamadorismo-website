# Generated by Django 3.2.10 on 2021-12-22 09:36

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repeaters', '0007_auto_20211222_0932'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dimdmr',
            name='ts1_tgs',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), null=True, size=None, verbose_name='TS1 TGs'),
        ),
        migrations.AlterField(
            model_name='dimdmr',
            name='ts2_tgs',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), null=True, size=None, verbose_name='TS2 TGs'),
        ),
    ]

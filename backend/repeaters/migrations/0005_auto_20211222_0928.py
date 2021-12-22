# Generated by Django 3.2.10 on 2021-12-22 09:28

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repeaters', '0004_auto_20211222_0926'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dimdmr',
            name='ts1_tgs',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), default=[1], size=None, verbose_name='TS1 TGs'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='dimdmr',
            name='ts2_tgs',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), default=[2], size=None, verbose_name='TS2 TGs'),
            preserve_default=False,
        ),
    ]
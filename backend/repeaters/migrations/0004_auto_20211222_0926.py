# Generated by Django 3.2.10 on 2021-12-22 09:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('repeaters', '0003_auto_20211222_0923'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dimdmr',
            name='ts1_tg_default',
        ),
        migrations.RemoveField(
            model_name='dimdmr',
            name='ts2_tg_default',
        ),
    ]

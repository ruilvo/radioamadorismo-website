# Generated by Django 4.2.5 on 2023-09-07 07:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("repeaters", "0016_remove_dimfm_unique_mod_tone_sql_combination_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="dimfm",
            name="ctcss_sql",
            field=models.BooleanField(default=False, verbose_name="CTCSS SQL"),
        ),
    ]

# Generated by Django 4.2.5 on 2023-09-07 07:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("repeaters", "0017_alter_dimfm_ctcss_sql"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="dimfm",
            name="unique mod./tone/SQL combination",
        ),
        migrations.AddField(
            model_name="dimfm",
            name="transit_pilot",
            field=models.DecimalField(
                blank=True,
                decimal_places=16,
                max_digits=32,
                null=True,
                verbose_name="transit pilot",
            ),
        ),
        migrations.AddConstraint(
            model_name="dimfm",
            constraint=models.UniqueConstraint(
                fields=(
                    "modulation",
                    "ctcss",
                    "ctcss_sql",
                    "transit_pilot",
                    "bandwidth",
                ),
                name="unique mod./tone/CTCSS SQL/transit pilot/bandwidth combination",
            ),
        ),
    ]
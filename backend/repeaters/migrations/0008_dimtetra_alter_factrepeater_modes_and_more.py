# Generated by Django 4.2.4 on 2023-08-24 18:05

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("repeaters", "0007_delete_dimholder"),
    ]

    operations = [
        migrations.CreateModel(
            name="DimTetra",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("mcc", models.IntegerField(verbose_name="MCC")),
                ("mnc", models.IntegerField(verbose_name="MNC")),
            ],
            options={
                "verbose_name": "info - TETRA",
                "verbose_name_plural": "info - TETRA",
            },
        ),
        migrations.AlterField(
            model_name="factrepeater",
            name="modes",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(
                    choices=[
                        ("fm", "FM"),
                        ("dmr", "DMR"),
                        ("dstar", "D-Star"),
                        ("fusion", "Fusion"),
                        ("tetra", "TETRA"),
                    ],
                    default=[],
                    max_length=64,
                    verbose_name="mode",
                ),
                editable=False,
                size=4,
            ),
        ),
        migrations.AddConstraint(
            model_name="dimtetra",
            constraint=models.UniqueConstraint(
                fields=("mcc", "mnc"), name="unique MCC/MNC combination"
            ),
        ),
        migrations.AddField(
            model_name="factrepeater",
            name="info_tetra",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.RESTRICT,
                to="repeaters.dimtetra",
                verbose_name="info - TETRA",
            ),
        ),
    ]

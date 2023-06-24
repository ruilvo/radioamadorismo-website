# Generated by Django 4.2.2 on 2023-06-24 12:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="DimDmr",
            fields=[
                (
                    "modulation",
                    models.CharField(
                        blank=True, max_length=20, verbose_name="modulation"
                    ),
                ),
                (
                    "id",
                    models.IntegerField(
                        primary_key=True,
                        serialize=False,
                        unique=True,
                        verbose_name="DMR ID",
                    ),
                ),
                ("color_code", models.IntegerField(verbose_name="C.C.")),
                (
                    "ts_configuration",
                    models.TextField(blank=True, verbose_name="TS config."),
                ),
            ],
            options={
                "verbose_name": "info - DMR",
                "verbose_name_plural": "info - DMR",
            },
        ),
        migrations.CreateModel(
            name="DimDmrTg",
            fields=[
                ("name", models.CharField(max_length=50, verbose_name="name")),
                (
                    "id",
                    models.IntegerField(
                        primary_key=True,
                        serialize=False,
                        unique=True,
                        verbose_name="DMR ID",
                    ),
                ),
                (
                    "call_mode",
                    models.CharField(
                        choices=[
                            ("GROUP_CALL", "Group Call"),
                            ("PRIVATE_CALL", "Private Call"),
                        ],
                        default="GROUP_CALL",
                        max_length=50,
                        verbose_name="call mode",
                    ),
                ),
            ],
            options={
                "verbose_name": "info - DMR TG",
                "verbose_name_plural": "info - DMR TG",
            },
        ),
        migrations.CreateModel(
            name="DimDStar",
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
                (
                    "modulation",
                    models.CharField(
                        blank=True, max_length=20, verbose_name="modulation"
                    ),
                ),
                (
                    "gateway",
                    models.CharField(blank=True, max_length=20, verbose_name="gateway"),
                ),
                (
                    "reflector",
                    models.CharField(
                        blank=True, max_length=50, verbose_name="reflector"
                    ),
                ),
            ],
            options={
                "verbose_name": "info - D-STAR",
                "verbose_name_plural": "info - D-STAR",
            },
        ),
        migrations.CreateModel(
            name="DimFm",
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
                (
                    "modulation",
                    models.CharField(
                        blank=True, max_length=20, verbose_name="modulation"
                    ),
                ),
                (
                    "tone",
                    models.DecimalField(
                        blank=True,
                        decimal_places=10,
                        max_digits=20,
                        null=True,
                        verbose_name="tone",
                    ),
                ),
                (
                    "bandwidth",
                    models.CharField(
                        choices=[("NFM", "narrow"), ("WFM", "wide")],
                        default="NFM",
                        max_length=50,
                        verbose_name="bandwidth",
                    ),
                ),
            ],
            options={
                "verbose_name": "info - FM",
                "verbose_name_plural": "info - FM",
            },
        ),
        migrations.CreateModel(
            name="DimFusion",
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
                (
                    "modulation",
                    models.CharField(
                        blank=True, max_length=20, verbose_name="modulation"
                    ),
                ),
                (
                    "wiresx",
                    models.CharField(blank=True, max_length=20, verbose_name="wiresx"),
                ),
                (
                    "room_id",
                    models.CharField(blank=True, max_length=20, verbose_name="room ID"),
                ),
            ],
            options={
                "verbose_name": "info - Fusion/C4FM",
                "verbose_name_plural": "info - Fusion/C4FM",
            },
        ),
        migrations.CreateModel(
            name="DimHalfDuplex",
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
                (
                    "tx_mhz",
                    models.DecimalField(
                        decimal_places=10, max_digits=20, verbose_name="tx (MHz)"
                    ),
                ),
                (
                    "rx_mhz",
                    models.DecimalField(
                        decimal_places=10, max_digits=20, verbose_name="rx (MHz)"
                    ),
                ),
                (
                    "channel",
                    models.CharField(
                        blank=True,
                        max_length=20,
                        null=True,
                        unique=True,
                        verbose_name="channel",
                    ),
                ),
            ],
            options={
                "verbose_name": "info - half-duplex",
                "verbose_name_plural": "info - half-duplex",
            },
        ),
        migrations.CreateModel(
            name="DimHolder",
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
                (
                    "abrv",
                    models.CharField(max_length=10, unique=True, verbose_name="abrv."),
                ),
                (
                    "name",
                    models.CharField(blank=True, max_length=500, verbose_name="name"),
                ),
            ],
            options={
                "verbose_name": "info - holder",
                "verbose_name_plural": "info - holders",
            },
        ),
        migrations.CreateModel(
            name="DimLocation",
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
                (
                    "latitude",
                    models.DecimalField(
                        blank=True,
                        decimal_places=10,
                        max_digits=20,
                        null=True,
                        verbose_name="latitude",
                    ),
                ),
                (
                    "longitude",
                    models.DecimalField(
                        blank=True,
                        decimal_places=10,
                        max_digits=20,
                        null=True,
                        verbose_name="longitude",
                    ),
                ),
                (
                    "region",
                    models.CharField(
                        choices=[
                            ("CPT", "Continental PT"),
                            ("AZR", "Azores"),
                            ("MDA", "Madeira"),
                            ("OT", "other"),
                        ],
                        default="CPT",
                        max_length=50,
                        verbose_name="region",
                    ),
                ),
                (
                    "place",
                    models.CharField(blank=True, max_length=500, verbose_name="place"),
                ),
                (
                    "qth_loc",
                    models.CharField(
                        blank=True, max_length=20, verbose_name="QTH loc."
                    ),
                ),
            ],
            options={
                "verbose_name": "info - location",
                "verbose_name_plural": "info - locations",
            },
        ),
        migrations.CreateModel(
            name="DimSimplex",
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
                (
                    "freq_mhz",
                    models.DecimalField(
                        decimal_places=10,
                        max_digits=20,
                        unique=True,
                        verbose_name="freq. (MHz)",
                    ),
                ),
                (
                    "channel",
                    models.CharField(
                        blank=True,
                        max_length=20,
                        null=True,
                        unique=True,
                        verbose_name="channel",
                    ),
                ),
            ],
            options={
                "verbose_name": "info - simplex",
                "verbose_name_plural": "info - simplex",
            },
        ),
        migrations.CreateModel(
            name="FactRepeater",
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
                ("callsign", models.CharField(max_length=10, verbose_name="callsign")),
                ("notes", models.TextField(blank=True, verbose_name="notes")),
                (
                    "pwr_w",
                    models.IntegerField(blank=True, null=True, verbose_name="pwr. (W)"),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("OFF", "off"),
                            ("ON", "on"),
                            ("PROJECT", "project"),
                            ("PROBLEMS", "problems"),
                            ("OT", "other"),
                        ],
                        default="OT",
                        max_length=50,
                        verbose_name="status",
                    ),
                ),
                (
                    "sysop",
                    models.CharField(blank=True, max_length=20, verbose_name="sysop"),
                ),
                (
                    "info_dmr",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="repeaters.dimdmr",
                        verbose_name="info - DMR",
                    ),
                ),
                (
                    "info_dstar",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="repeaters.dimdstar",
                        verbose_name="info - D-STAR",
                    ),
                ),
                (
                    "info_fm",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="repeaters.dimfm",
                        verbose_name="info - FM",
                    ),
                ),
                (
                    "info_fusion",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="repeaters.dimfusion",
                        verbose_name="info - Fusion/C4FM",
                    ),
                ),
                (
                    "info_half_duplex",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="repeaters.dimhalfduplex",
                        verbose_name="info - half-duplex",
                    ),
                ),
                (
                    "info_holder",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="repeaters.dimholder",
                        verbose_name="info - holder",
                    ),
                ),
                (
                    "info_location",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="repeaters.dimlocation",
                        verbose_name="info - location",
                    ),
                ),
                (
                    "info_simplex",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="repeaters.dimsimplex",
                        verbose_name="info - simplex",
                    ),
                ),
            ],
            options={
                "verbose_name": "repeater",
                "verbose_name_plural": "repeaters",
            },
        ),
        migrations.AddConstraint(
            model_name="dimlocation",
            constraint=models.UniqueConstraint(
                fields=("latitude", "longitude"), name="unique lat./long. combination"
            ),
        ),
        migrations.AddConstraint(
            model_name="dimhalfduplex",
            constraint=models.UniqueConstraint(
                fields=("tx_mhz", "rx_mhz"), name="unique tx/rx combination"
            ),
        ),
        migrations.AddConstraint(
            model_name="dimfusion",
            constraint=models.UniqueConstraint(
                fields=("wiresx", "room_id"), name="unique wiresx/room_id combination"
            ),
        ),
        migrations.AddConstraint(
            model_name="dimfm",
            constraint=models.UniqueConstraint(
                fields=("modulation", "tone"), name="unique mod./tone combination"
            ),
        ),
        migrations.AddConstraint(
            model_name="dimdstar",
            constraint=models.UniqueConstraint(
                fields=("gateway", "reflector"),
                name="unique gateway/reflector combination",
            ),
        ),
        migrations.AddField(
            model_name="dimdmr",
            name="ts1_alternative_tgs",
            field=models.ManyToManyField(
                blank=True,
                related_name="%(class)s_ts1_alternative_tgs",
                to="repeaters.dimdmrtg",
            ),
        ),
        migrations.AddField(
            model_name="dimdmr",
            name="ts1_default_tg",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="%(class)s_ts1_default_tg",
                to="repeaters.dimdmrtg",
            ),
        ),
        migrations.AddField(
            model_name="dimdmr",
            name="ts2_alternative_tgs",
            field=models.ManyToManyField(
                blank=True,
                related_name="%(class)s_ts2_alternative_tgs",
                to="repeaters.dimdmrtg",
            ),
        ),
        migrations.AddField(
            model_name="dimdmr",
            name="ts2_default_tg",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="%(class)s_ts2_default_tg",
                to="repeaters.dimdmrtg",
            ),
        ),
        migrations.AddConstraint(
            model_name="factrepeater",
            constraint=models.CheckConstraint(
                check=models.Q(
                    models.Q(("info_half_duplex", None), ("info_simplex", None)),
                    models.Q(
                        models.Q(("info_half_duplex", None), _negated=True),
                        ("info_simplex", None),
                    ),
                    models.Q(
                        ("info_half_duplex", None),
                        models.Q(("info_simplex", None), _negated=True),
                    ),
                    _connector="OR",
                ),
                name="repeater is only simplex or half-duplex",
            ),
        ),
    ]

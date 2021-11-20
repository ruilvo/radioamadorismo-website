from django.db import models

# Create your models here.

# RF ----


class DimHalfDuplex(models.Model):
    tx_mhz = models.DecimalField(
        max_digits=20, decimal_places=10, verbose_name="tx (MHz)"
    )
    rx_mhz = models.DecimalField(
        max_digits=20, decimal_places=10, verbose_name="rx (MHz)"
    )
    channel = models.CharField(
        max_length=20, blank=True, null=True, unique=True, verbose_name="channel"
    )

    class Meta:
        verbose_name = "info - half-duplex"
        verbose_name_plural = "info - half-duplex"
        constraints = [
            models.UniqueConstraint(
                fields=["tx_mhz", "rx_mhz"], name="unique tx/rx combination"
            )
        ]

    @property
    def shift(self):
        return self.tx_mhz - self.rx_mhz

    def __str__(self) -> str:
        return f"{self.tx_mhz}/{self.rx_mhz}"


class DimSimplex(models.Model):
    freq_mhz = models.DecimalField(
        max_digits=20, decimal_places=10, unique=True, verbose_name="freq. (MHz)"
    )
    channel = models.CharField(
        max_length=20, blank=True, null=True, unique=True, verbose_name="channel"
    )

    class Meta:
        verbose_name = "info - simplex"
        verbose_name_plural = "info - simplex"

    def __str__(self) -> str:
        return f"{self.freq_mhz}"


# Modulacao ----


class DimFm(models.Model):
    modulation = models.CharField(max_length=20, blank=True, verbose_name="modulation")
    tone = models.DecimalField(
        max_digits=20, decimal_places=10, blank=True, null=True, verbose_name="tone"
    )

    class Meta:
        verbose_name = "info - FM"
        verbose_name_plural = "info - FM"
        constraints = [
            models.UniqueConstraint(
                fields=["modulation", "tone"], name="unique mod./tone combination"
            )
        ]

    def __str__(self) -> str:
        return f"{self.modulation}, {self.tone}"


class DimDStar(models.Model):
    modulation = models.CharField(max_length=20, blank=True, verbose_name="modulation")
    gateway = models.CharField(max_length=20, blank=True, verbose_name="gateway")
    reflector = models.CharField(max_length=50, blank=True, verbose_name="reflector")

    class Meta:
        verbose_name = "info - D-STAR"
        verbose_name_plural = "info - D-STAR"
        constraints = [
            models.UniqueConstraint(
                fields=["gateway", "reflector"],
                name="unique gateway/reflector combination",
            )
        ]

    def __str__(self) -> str:
        return f"{self.modulation}, {self.gateway}, {self.reflector}"


class DimFusion(models.Model):
    modulation = models.CharField(max_length=20, blank=True, verbose_name="modulation")
    wiresx = models.CharField(max_length=20, blank=True, verbose_name="wiresx")
    room_id = models.CharField(max_length=20, blank=True, verbose_name="room ID")

    class Meta:
        verbose_name = "info - Fusion/C4FM"
        verbose_name_plural = "info - Fusion/C4FM"
        constraints = [
            models.UniqueConstraint(
                fields=["wiresx", "room_id"],
                name="unique wiresx/room_id combination",
            )
        ]

    def __str__(self) -> str:
        return f"{self.wiresx}, {self.room_id}"


class DimDmr(models.Model):
    modulation = models.CharField(max_length=20, blank=True, verbose_name="modulation")
    dmr_id = models.IntegerField(unique=True, verbose_name="DMR ID")
    color_code = models.IntegerField(verbose_name="C.C.")
    ts1_configuration = models.TextField(blank=True, verbose_name="TS1 config.")
    ts2_configuration = models.TextField(blank=True, verbose_name="TS2 config.")

    class Meta:
        verbose_name = "info - DMR"
        verbose_name_plural = "info - DMR"

    def __str__(self) -> str:
        return f"{self.dmr_id}"


# Info ----


class DimHolder(models.Model):
    abrv = models.CharField(max_length=10, verbose_name="abrv.", unique=True)
    name = models.CharField(max_length=500, blank=True, verbose_name="name")

    class Meta:
        verbose_name = "info - holder"
        verbose_name_plural = "info - holders"

    def __str__(self) -> str:
        return f"{self.abrv}"


class DimLocation(models.Model):
    CONTINENT = "CPT"
    AZORES = "AZR"
    MADEIRA = "MDA"
    OTHER = "OT"
    REGION_CHOICES = (
        (CONTINENT, "Continental PT"),
        (AZORES, "Azores"),
        (MADEIRA, "Madeira"),
        (OTHER, "other"),
    )

    # In the future, update this to GeoDjango
    # https://docs.djangoproject.com/en/3.2/ref/contrib/gis/
    latitude = models.DecimalField(
        max_digits=20, decimal_places=10, blank=True, null=True, verbose_name="latitude"
    )
    longitude = models.DecimalField(
        max_digits=20,
        decimal_places=10,
        blank=True,
        null=True,
        verbose_name="longitude",
    )
    # -
    region = models.CharField(
        max_length=50, verbose_name="region", choices=REGION_CHOICES, default=CONTINENT
    )
    place = models.CharField(max_length=500, blank=True, verbose_name="place")
    qth_loc = models.CharField(max_length=20, blank=True, verbose_name="QTH loc.")

    class Meta:
        verbose_name = "info - location"
        verbose_name_plural = "info - locations"
        constraints = [
            models.UniqueConstraint(
                fields=["latitude", "longitude"], name="unique lat./long. combination"
            )
        ]

    def __str__(self) -> str:
        to_return = ""
        if self.place is not None:
            to_return += f"{self.place}"
        if self.qth_loc is not None:
            to_return += f"/{self.qth_loc}"
        if self.latitude is not None and self.longitude is not None:
            to_return += f"/({self.latitude}, {self.longitude})"
        return to_return


# Base ----


class FactRepeater(models.Model):
    callsign = models.CharField(max_length=10, verbose_name="callsign")
    notes = models.TextField(blank=True, verbose_name="notes")
    sysop = models.CharField(max_length=20, blank=True, verbose_name="sysop")
    pwr_w = models.IntegerField(blank=True, null=True, verbose_name="pwr. (W)")

    # E agora dados opcionais
    # RF
    info_half_duplex = models.ForeignKey(
        DimHalfDuplex,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="info - half-duplex",
    )
    info_simplex = models.ForeignKey(
        DimSimplex,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="info - simplex",
    )
    # Modulacao
    info_fm = models.ForeignKey(
        DimFm,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="info - FM",
    )
    info_dstar = models.ForeignKey(
        DimDStar,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="info - D-STAR",
    )
    info_fusion = models.ForeignKey(
        DimFusion,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="info - Fusion/C4FM",
    )
    info_dmr = models.ForeignKey(
        DimDmr,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="info - DMR",
    )
    # Info
    info_holder = models.ForeignKey(
        DimHolder,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="info - holder",
    )
    info_location = models.ForeignKey(
        DimLocation,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="info - location",
    )

    class Meta:
        verbose_name = "repeater"
        verbose_name_plural = "repeaters"
        constraints = [
            models.CheckConstraint(
                check=(
                    (models.Q(info_half_duplex=None) & models.Q(info_simplex=None))
                    | (~models.Q(info_half_duplex=None) & models.Q(info_simplex=None))
                    | (models.Q(info_half_duplex=None) & ~models.Q(info_simplex=None))
                ),
                name="repeater is only simplex or half-duplex",
            )
        ]

    def __str__(self) -> str:
        return self.callsign

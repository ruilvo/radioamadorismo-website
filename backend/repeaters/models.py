import decimal

from django.db import models

str_placeholder = "-----"


class DimHalfDuplex(models.Model):
    """
    Models enough information for describing half-duplex repeaters.
    """

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
    def shift(self) -> decimal.Decimal:
        return self.tx_mhz - self.rx_mhz

    def __str__(self) -> str:
        return (
            f"{self.channel if self.channel else str_placeholder}: "
            + f"{float(self.tx_mhz):.5f}/{float(self.rx_mhz):.5f}"
        )


class DimSimplex(models.Model):
    """
    Models enough information for describing simplex repeaters.
    """

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
        return (
            f"{self.channel if self.channel else str_placeholder}: "
            + f"{float(self.freq_mhz):.5f}"
        )


class DimFm(models.Model):
    """
    Models enough information for describing FM repeaters.
    """

    NFM = "NFM"
    WFM = "WFM"
    BANDWIDTH_CHOICES = (
        (NFM, "NFM"),
        (WFM, "WFM"),
    )

    modulation = models.CharField(max_length=20, blank=True, verbose_name="modulation")
    tone = models.DecimalField(
        max_digits=20, decimal_places=10, blank=True, null=True, verbose_name="tone"
    )
    bandwidth = models.CharField(
        max_length=50, verbose_name="bandwidth", choices=BANDWIDTH_CHOICES, default=NFM
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
        return (
            f"{self.modulation if self.modulation else str_placeholder}, "
            + f"{float(self.tone):.1f}, "
            + f"{self.bandwidth}"
        )


class DimDStar(models.Model):
    """
    Models enough information for describing D-STAR repeaters.
    """

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
        return (
            f"{self.modulation if self.modulation else str_placeholder}, "
            + f"{self.gateway if self.gateway else str_placeholder}, "
            + f"{self.reflector if self.reflector else str_placeholder}"
        )


class DimFusion(models.Model):
    """
    Models enough information for describing Fusion/C4FM repeaters.
    """

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
        return (
            f"{self.modulation if self.modulation else str_placeholder}, "
            + f"{self.wiresx if self.wiresx else str_placeholder}, "
            + f"{self.room_id if self.room_id else str_placeholder}"
        )


class DimDmrTg(models.Model):
    """
    Models enough information for describing a DMR TG.
    """

    name = models.CharField(max_length=50, verbose_name="name")
    dmr_id = models.IntegerField(unique=True, verbose_name="DMR ID")

    class Meta:
        verbose_name = "info - DMR TG"
        verbose_name_plural = "info - DMR TG"

    def __str__(self) -> str:
        return f"{self.dmr_id}: {self.name}"


class DimDmr(models.Model):
    """
    Models enough information for describing DMR repeaters.
    """

    modulation = models.CharField(max_length=20, blank=True, verbose_name="modulation")
    dmr_id = models.IntegerField(unique=True, verbose_name="DMR ID")
    color_code = models.IntegerField(verbose_name="C.C.")
    ts1_default_tg = models.ForeignKey(
        DimDmrTg,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="%(class)s_ts1_default_tg",
    )
    ts2_default_tg = models.ForeignKey(
        DimDmrTg,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="%(class)s_ts2_default_tg",
    )
    ts1_alternative_tgs = models.ManyToManyField(
        DimDmrTg,
        blank=True,
        related_name="%(class)s_ts1_alternative_tgs",
    )
    ts2_alternative_tgs = models.ManyToManyField(
        DimDmrTg,
        blank=True,
        related_name="%(class)s_ts2_alternative_tgs",
    )
    ts_configuration = models.TextField(blank=True, verbose_name="TS config.")

    class Meta:
        verbose_name = "info - DMR"
        verbose_name_plural = "info - DMR"

    def __str__(self) -> str:
        return f"{self.dmr_id}"


class DimHolder(models.Model):
    """
    Models enough information for describing the holder of a repeater.
    """

    abrv = models.CharField(max_length=10, verbose_name="abrv.", unique=True)
    name = models.CharField(max_length=500, blank=True, verbose_name="name")

    class Meta:
        verbose_name = "info - holder"
        verbose_name_plural = "info - holders"

    def __str__(self) -> str:
        return f"{self.abrv}: {self.name if self.name else str_placeholder}"


class DimLocation(models.Model):
    """
    Models enough information for describing a repeater's location.
    """

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
        coordinates_str = ""
        if self.latitude is not None and self.longitude is not None:
            coordinates_str = f" ({self.latitude}, {self.longitude})"
        return (
            f"{self.region if self.region else str_placeholder}, "
            + f"{self.place if self.place else str_placeholder}, "
            + f"{self.qth_loc if self.qth_loc else str_placeholder}, "
            + coordinates_str
        )


class FactRepeater(models.Model):
    """
    Models a repeater's full information.
    """

    OFF = "OFF"
    ON = "ON"
    PROJECT = "PROJECT"
    PROBLEMS = "PROBLEMS"
    OTHER = "OT"
    STATUS_CHOICES = (
        (OFF, "OFF"),
        (ON, "ON"),
        (PROJECT, "PROJECT"),
        (PROBLEMS, "PROBLEMS"),
        (OTHER, "other"),
    )

    callsign = models.CharField(max_length=10, verbose_name="callsign")
    notes = models.TextField(blank=True, verbose_name="notes")
    pwr_w = models.IntegerField(blank=True, null=True, verbose_name="pwr. (W)")
    status = models.CharField(
        max_length=50, verbose_name="status", choices=STATUS_CHOICES, default=OTHER
    )
    sysop = models.CharField(max_length=20, blank=True, verbose_name="sysop")

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
    # Modulation
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
        return str(self.callsign)

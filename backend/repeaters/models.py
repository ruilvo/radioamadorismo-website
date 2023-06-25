import decimal

from typing import Optional

from django.db import models

from computedfields.models import ComputedFieldsModel, computed

from repeaters.vendor.bands import Band23cm, Band70cm, Band2m, Band6m, Band10m

str_placeholder = "-----"


class DimHalfDuplex(models.Model):
    """
    Models enough information for describing half-duplex repeaters.
    """

    tx_mhz = models.DecimalField(
        max_digits=32, decimal_places=16, verbose_name="tx (MHz)"
    )
    rx_mhz = models.DecimalField(
        max_digits=32, decimal_places=16, verbose_name="rx (MHz)"
    )
    channel = models.CharField(
        max_length=32, blank=True, null=True, unique=True, verbose_name="channel"
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
        max_digits=32, decimal_places=16, unique=True, verbose_name="freq. (MHz)"
    )
    channel = models.CharField(
        max_length=32, blank=True, null=True, unique=True, verbose_name="channel"
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

    class BandwidthOptions:
        NFM = "NFM"
        WFM = "WFM"

    BANDWIDTH_CHOICES = (
        (BandwidthOptions.NFM, "narrow"),
        (BandwidthOptions.WFM, "wide"),
    )

    modulation = models.CharField(max_length=32, blank=True, verbose_name="modulation")
    tone = models.DecimalField(
        max_digits=32, decimal_places=16, blank=True, null=True, verbose_name="tone"
    )
    bandwidth = models.CharField(
        max_length=64,
        verbose_name="bandwidth",
        choices=BANDWIDTH_CHOICES,
        default=BandwidthOptions.NFM,
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

    modulation = models.CharField(max_length=32, blank=True, verbose_name="modulation")
    gateway = models.CharField(max_length=32, blank=True, verbose_name="gateway")
    reflector = models.CharField(max_length=64, blank=True, verbose_name="reflector")

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

    modulation = models.CharField(max_length=32, blank=True, verbose_name="modulation")
    wiresx = models.CharField(max_length=32, blank=True, verbose_name="wiresx")
    room_id = models.CharField(max_length=32, blank=True, verbose_name="room ID")

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

    class CallModeOptions:
        GROUP_CALL = "GROUP_CALL"
        PRIVATE_CALL = "PRIVATE_CALL"

    CALL_MODE_CHOICES = (
        (CallModeOptions.GROUP_CALL, "Group Call"),
        (CallModeOptions.PRIVATE_CALL, "Private Call"),
    )

    name = models.CharField(max_length=64, verbose_name="name")
    id = models.IntegerField(unique=True, verbose_name="DMR ID", primary_key=True)
    call_mode = models.CharField(
        max_length=64,
        verbose_name="call mode",
        choices=CALL_MODE_CHOICES,
        default=CallModeOptions.GROUP_CALL,
    )

    class Meta:
        verbose_name = "info - DMR TG"
        verbose_name_plural = "info - DMR TG"

    def __str__(self) -> str:
        return f"{self.id}: {self.name}"


class DimDmr(models.Model):
    """
    Models enough information for describing DMR repeaters.
    """

    modulation = models.CharField(max_length=32, blank=True, verbose_name="modulation")
    id = models.IntegerField(unique=True, verbose_name="DMR ID", primary_key=True)
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
        return f"{self.id}"


class DimHolder(models.Model):
    """
    Models enough information for describing the holder of a repeater.
    """

    abrv = models.CharField(max_length=16, verbose_name="abrv.", unique=True)
    name = models.CharField(max_length=512, blank=True, verbose_name="name")

    class Meta:
        verbose_name = "info - holder"
        verbose_name_plural = "info - holders"

    def __str__(self) -> str:
        return f"{self.abrv}: {self.name if self.name else str_placeholder}"


class DimLocation(models.Model):
    """
    Models enough information for describing a repeater's location.
    """

    class RegionOptions:
        CONTINENT = "CPT"
        AZORES = "AZR"
        MADEIRA = "MDA"
        OTHER = "OT"

    REGION_CHOICES = (
        (RegionOptions.CONTINENT, "Continental PT"),
        (RegionOptions.AZORES, "Azores"),
        (RegionOptions.MADEIRA, "Madeira"),
        (RegionOptions.OTHER, "other"),
    )

    # In the future, update this to GeoDjango
    # https://docs.djangoproject.com/en/3.2/ref/contrib/gis/
    latitude = models.DecimalField(
        max_digits=32, decimal_places=16, blank=True, null=True, verbose_name="latitude"
    )
    longitude = models.DecimalField(
        max_digits=32,
        decimal_places=16,
        blank=True,
        null=True,
        verbose_name="longitude",
    )
    region = models.CharField(
        max_length=64,
        verbose_name="region",
        choices=REGION_CHOICES,
        default=RegionOptions.CONTINENT,
    )
    place = models.CharField(max_length=512, blank=True, verbose_name="place")
    qth_loc = models.CharField(max_length=32, blank=True, verbose_name="QTH loc.")

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


class FactRepeater(ComputedFieldsModel):
    """
    Models a repeater's full information.
    """

    class StatusOptions:
        OFF = "OFF"
        ON = "ON"
        PROJECT = "PROJECT"
        PROBLEMS = "PROBLEMS"
        OTHER = "OT"

    STATUS_CHOICES = (
        (StatusOptions.OFF, "off"),
        (StatusOptions.ON, "on"),
        (StatusOptions.PROJECT, "project"),
        (StatusOptions.PROBLEMS, "problems"),
        (StatusOptions.OTHER, "other"),
    )

    class BandOptions:
        B_10M = "10m"
        B_6M = "6m"
        B_2M = "2m"
        B_70CM = "70cm"
        B_23CM = "23cm"
        B_X = "X"
        B_OTHER = "OT"

    BAND_CHOICES = (
        (BandOptions.B_10M, "10m"),
        (BandOptions.B_6M, "6m"),
        (BandOptions.B_2M, "2m"),
        (BandOptions.B_70CM, "70cm"),
        (BandOptions.B_23CM, "23cm"),
        (BandOptions.B_X, "cross-band"),
        (BandOptions.B_OTHER, "other"),
    )

    callsign = models.CharField(max_length=16, verbose_name="callsign")
    notes = models.TextField(blank=True, verbose_name="notes")
    pwr_w = models.IntegerField(blank=True, null=True, verbose_name="pwr. (W)")
    status = models.CharField(
        max_length=64,
        verbose_name="status",
        choices=STATUS_CHOICES,
        default=StatusOptions.OTHER,
    )
    sysop = models.CharField(max_length=32, blank=True, verbose_name="sysop")

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

    @property
    def is_simplex(self) -> bool:
        return self.info_simplex is not None

    @property
    def is_half_duplex(self) -> bool:
        return self.info_half_duplex is not None

    @property
    def has_rf(self) -> bool:
        return self.is_half_duplex or self.is_simplex

    @computed(
        # TODO(ruilvo): change this to a CharField with choices.
        # Related: use the choices for the filter.
        models.CharField(max_length=64, blank=True, null=True, verbose_name="RF"),
        depends=[("self", ["info_simplex", "info_half_duplex"])],
    )
    def rf(self) -> Optional[str]:
        if self.is_simplex:
            return "simplex"
        if self.is_half_duplex:
            return "half-duplex"
        return None

    @property
    def tx_freq(self) -> Optional[float]:
        if self.is_simplex:
            return self.info_simplex.freq_mhz
        if self.is_half_duplex:
            return self.info_half_duplex.tx_mhz
        return None

    @property
    def rx_freq(self) -> Optional[float]:
        if self.is_simplex:
            return self.info_simplex.freq_mhz
        if self.is_half_duplex:
            return self.info_half_duplex.rx_mhz
        return None

    @computed(
        # TODO(ruilvo): create a filter for this.
        models.CharField(
            max_length=64,
            verbose_name="band",
            choices=BAND_CHOICES,
            default=BandOptions.B_OTHER,
            blank=True,
            null=True,
        ),
        depends=[("self", ["info_simplex", "info_half_duplex"])],
    )
    def band(self) -> Optional[str]:
        def get_band_for_freq(f_mhz: float) -> Optional[str]:
            if f_mhz is None:
                return None
            if Band10m.min <= f_mhz <= Band10m.max:
                return self.BandOptions.B_10M
            if Band6m.min <= f_mhz <= Band6m.max:
                return self.BandOptions.B_6M
            if Band2m.min <= f_mhz <= Band2m.max:
                return self.BandOptions.B_2M
            if Band70cm.min <= f_mhz <= Band70cm.max:
                return self.BandOptions.B_70CM
            if Band23cm.min <= f_mhz <= Band23cm.max:
                return self.BandOptions.B_23CM
            return None

        tx_band = get_band_for_freq(self.tx_freq)
        rx_band = get_band_for_freq(self.rx_freq)

        # If the Tx and Rx bands are the same, return that band.
        if tx_band == rx_band:
            return tx_band

        # If they are different, it's a cross-band repeater.
        if tx_band is not None and rx_band is not None:
            return self.BandOptions.B_X

        # If either is None, return other.
        return self.BandOptions.B_OTHER

    @property
    def is_fm(self) -> bool:
        return self.info_fm is not None

    @property
    def is_dstar(self) -> bool:
        return self.info_dstar is not None

    @property
    def is_fusion(self) -> bool:
        return self.info_fusion is not None

    @property
    def is_dmr(self) -> bool:
        return self.info_dmr is not None

    @property
    def has_modulation(self) -> bool:
        return self.is_fm or self.is_dstar or self.is_fusion or self.is_dmr

    @computed(
        # TODO(ruilvo): Use the choices for the filter.
        models.CharField(max_length=64, blank=True, null=True, verbose_name="mode"),
        depends=[("self", ["info_fm", "info_dstar", "info_fusion", "info_dmr"])],
    )
    def mode(self) -> Optional[str]:
        if self.is_fm:
            return "fm"
        if self.is_dstar:
            return "dstar"
        if self.is_fusion:
            return "fusion"
        if self.is_dmr:
            return "dmr"
        return None

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

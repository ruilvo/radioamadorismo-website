"""
Django models definition for the repeaters app of the radioamadorismo-web project.
"""

import decimal

from typing import Optional

from django.db import models
from django.contrib.postgres.fields import ArrayField

from computedfields.models import ComputedFieldsModel, computed

from django_admin_geomap import GeoItem

from associations.models import Association

from repeaters.vendor.bands import Band23cm, Band70cm, Band2m, Band6m, Band10m

PLACEHOLDER_STR = "-----"


class DimRf(ComputedFieldsModel):
    """
    Models the frequency information of repeaters.
    """

    class BandOptions:  # pylint: disable=too-few-public-methods
        """
        Band options for the RF information of repeaters.
        """

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

    class ModeOptions:  # pylint: disable=too-few-public-methods
        """
        Mode options for the RF information of repeaters.
        """

        HALF_DUPLEX = "HD"
        SIMPLEX = "SX"

    MODE_CHOICES = (
        (ModeOptions.HALF_DUPLEX, "half-duplex"),
        (ModeOptions.SIMPLEX, "simplex"),
    )

    tx_mhz = models.DecimalField(
        max_digits=32, decimal_places=16, verbose_name="tx (MHz)"
    )
    rx_mhz = models.DecimalField(
        max_digits=32, decimal_places=16, verbose_name="rx (MHz)"
    )
    channel = models.CharField(
        max_length=32, blank=True, null=True, unique=True, verbose_name="channel"
    )

    @computed(
        models.CharField(
            max_length=64,
            verbose_name="band",
            choices=BAND_CHOICES,
            default=BandOptions.B_OTHER,
        )
    )
    def band(self) -> Optional[str]:
        """
        Computes the band of the repeater based on the tx and rx frequencies.
        """
        tx_band = self._get_band_for_freq(self.tx_mhz)
        rx_band = self._get_band_for_freq(self.rx_mhz)

        # If any of the bands is "other", return "other".
        if DimRf.BandOptions.B_OTHER in {tx_band, rx_band}:
            return DimRf.BandOptions.B_OTHER

        # If the Tx and Rx bands are the same, return that band.
        if tx_band == rx_band:
            return tx_band

        # If they are different, it's a cross-band repeater.
        return self.BandOptions.B_X

    @computed(
        models.CharField(
            max_length=64,
            verbose_name="mode",
            choices=MODE_CHOICES,
            default=ModeOptions.SIMPLEX,
        ),
    )
    def mode(self) -> str:
        """
        Computes the mode of the repeater based on the tx and rx frequencies.
        """
        if self.tx_mhz == self.rx_mhz:
            return DimRf.ModeOptions.SIMPLEX
        return DimRf.ModeOptions.HALF_DUPLEX

    @computed(
        models.DecimalField(
            max_digits=32, decimal_places=16, verbose_name="shift (MHz)"
        )
    )
    def shift_mhz(self) -> decimal.Decimal:
        """
        Computes the shift of the repeater based on the tx and rx frequencies.
        """
        return self.tx_mhz - self.rx_mhz

    def __str__(self) -> str:
        return (
            f"{self.channel if self.channel else PLACEHOLDER_STR}: "
            + f"{float(self.tx_mhz):.5f}/{float(self.rx_mhz):.5f}"
        )

    def _get_band_for_freq(  # pylint: disable=too-many-return-statements
        self,
        f_mhz: float,
    ) -> Optional[str]:
        """
        Returns the band for a given frequency in MHz.
        """
        if f_mhz is None:
            return None
        if Band10m.min <= f_mhz <= Band10m.max:
            return DimRf.BandOptions.B_10M
        if Band6m.min <= f_mhz <= Band6m.max:
            return DimRf.BandOptions.B_6M
        if Band2m.min <= f_mhz <= Band2m.max:
            return DimRf.BandOptions.B_2M
        if Band70cm.min <= f_mhz <= Band70cm.max:
            return DimRf.BandOptions.B_70CM
        if Band23cm.min <= f_mhz <= Band23cm.max:
            return DimRf.BandOptions.B_23CM
        return DimRf.BandOptions.B_OTHER

    class Meta:
        verbose_name = "info - RF"
        verbose_name_plural = "info - RF"
        constraints = [
            models.UniqueConstraint(
                fields=["tx_mhz", "rx_mhz"], name="unique tx/rx combination"
            )
        ]


class DimFm(models.Model):
    """
    Models enough information for describing FM repeaters.
    """

    class BandwidthOptions:  # pylint: disable=too-few-public-methods
        """
        Define the bandwidth options for FM repeaters.
        """

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

    def __str__(self) -> str:
        return (
            f"{self.modulation if self.modulation else PLACEHOLDER_STR}, "
            + f"{float(self.tone):.1f}, "
            + f"{self.bandwidth}"
        )

    class Meta:
        verbose_name = "info - FM"
        verbose_name_plural = "info - FM"
        constraints = [
            models.UniqueConstraint(
                fields=["modulation", "tone"], name="unique mod./tone combination"
            )
        ]


class DimDStar(models.Model):
    """
    Models enough information for describing D-STAR repeaters.
    """

    modulation = models.CharField(max_length=32, blank=True, verbose_name="modulation")
    gateway = models.CharField(max_length=32, blank=True, verbose_name="gateway")
    reflector = models.CharField(max_length=64, blank=True, verbose_name="reflector")

    def __str__(self) -> str:
        return (
            f"{self.modulation if self.modulation else PLACEHOLDER_STR}, "
            + f"{self.gateway if self.gateway else PLACEHOLDER_STR}, "
            + f"{self.reflector if self.reflector else PLACEHOLDER_STR}"
        )

    class Meta:
        verbose_name = "info - D-STAR"
        verbose_name_plural = "info - D-STAR"
        constraints = [
            models.UniqueConstraint(
                fields=["gateway", "reflector"],
                name="unique gateway/reflector combination",
            )
        ]


class DimFusion(models.Model):
    """
    Models enough information for describing Fusion/C4FM repeaters.
    """

    modulation = models.CharField(max_length=32, blank=True, verbose_name="modulation")
    wiresx = models.CharField(max_length=32, blank=True, verbose_name="wiresx")
    room_id = models.CharField(max_length=32, blank=True, verbose_name="room ID")

    def __str__(self) -> str:
        return (
            f"{self.modulation if self.modulation else PLACEHOLDER_STR}, "
            + f"{self.wiresx if self.wiresx else PLACEHOLDER_STR}, "
            + f"{self.room_id if self.room_id else PLACEHOLDER_STR}"
        )

    class Meta:
        verbose_name = "info - Fusion/C4FM"
        verbose_name_plural = "info - Fusion/C4FM"
        constraints = [
            models.UniqueConstraint(
                fields=["wiresx", "room_id"],
                name="unique wiresx/room_id combination",
            )
        ]


class DimDmrTg(models.Model):
    """
    Models enough information for describing a DMR TG.
    """

    class CallModeOptions:  # pylint: disable=too-few-public-methods
        """
        Define the call mode options for DMR TGs.
        """

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

    def __str__(self) -> str:
        return f"{self.id}: {self.name}"

    class Meta:
        verbose_name = "info - DMR TG"
        verbose_name_plural = "info - DMR TG"


class DimDmr(models.Model):
    """
    Models enough information for describing DMR repeaters.
    """

    modulation = models.CharField(max_length=32, blank=True, verbose_name="modulation")
    # A DMR repeater has an unique DMR TG associated.
    tg = models.ForeignKey(DimDmrTg, on_delete=models.RESTRICT)
    color_code = models.IntegerField(verbose_name="C.C.")
    ts1_default_tg = models.ForeignKey(
        DimDmrTg,
        on_delete=models.RESTRICT,
        related_name="%(class)s_ts1_default_tg",
    )
    ts2_default_tg = models.ForeignKey(
        DimDmrTg,
        on_delete=models.RESTRICT,
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

    def __str__(self) -> str:
        return f"{self.tg.id}: {self.tg.name}"

    class Meta:
        verbose_name = "info - DMR"
        verbose_name_plural = "info - DMR"


class DimTetra(models.Model):
    """
    Models enough information for describing TETRA repeaters.
    """

    mcc = models.IntegerField(verbose_name="MCC")
    mnc = models.IntegerField(verbose_name="MNC")

    class Meta:
        verbose_name = "info - TETRA"
        verbose_name_plural = "info - TETRA"
        constraints = [
            models.UniqueConstraint(
                fields=["mcc", "mnc"], name="unique MCC/MNC combination"
            )
        ]


class DimLocation(models.Model, GeoItem):
    """
    Models enough information for describing a repeater's location.
    """

    class RegionOptions:  # pylint: disable=too-few-public-methods
        """
        Define the region options for a repeater's location.
        """

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

    @property
    def geomap_longitude(self):
        return "" if self.longitude is None else str(self.longitude)

    @property
    def geomap_latitude(self):
        return "" if self.latitude is None else str(self.latitude)

    def __str__(self) -> str:
        coordinates_str = PLACEHOLDER_STR
        if self.latitude is not None and self.longitude is not None:
            coordinates_str = f" ({self.latitude:.4f}, {self.longitude:.4f})"
        return (
            f"{self.region if self.region else PLACEHOLDER_STR}, "
            + f"{self.place if self.place else PLACEHOLDER_STR}, "
            + f"{self.qth_loc if self.qth_loc else PLACEHOLDER_STR}, "
            + coordinates_str
        )

    class Meta:
        verbose_name = "info - location"
        verbose_name_plural = "info - locations"
        constraints = [
            models.UniqueConstraint(
                fields=["latitude", "longitude"], name="unique lat./long. combination"
            )
        ]


class FactRepeater(ComputedFieldsModel):
    """
    Models a repeater's full information.
    """

    class StatusOptions:  # pylint: disable=too-few-public-methods
        """
        Define the status options for a repeater.
        """

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

    class ModeOptions:  # pylint: disable=too-few-public-methods
        """
        Define the mode options for a repeater.
        """

        FM = "fm"
        DMR = "dmr"
        DSTAR = "dstar"
        FUSION = "fusion"
        TETRA = "tetra"

    MODE_CHOICES = (
        (ModeOptions.FM, "FM"),
        (ModeOptions.DMR, "DMR"),
        (ModeOptions.DSTAR, "D-Star"),
        (ModeOptions.FUSION, "Fusion"),
        (ModeOptions.TETRA, "TETRA"),
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
    info_rf = models.ForeignKey(
        DimRf,
        on_delete=models.RESTRICT,
        verbose_name="info - RF",
    )

    # Modulation
    info_fm = models.ForeignKey(
        DimFm,
        on_delete=models.RESTRICT,
        blank=True,
        null=True,
        verbose_name="info - FM",
    )
    info_dstar = models.ForeignKey(
        DimDStar,
        on_delete=models.RESTRICT,
        blank=True,
        null=True,
        verbose_name="info - D-STAR",
    )
    info_fusion = models.ForeignKey(
        DimFusion,
        on_delete=models.RESTRICT,
        blank=True,
        null=True,
        verbose_name="info - Fusion/C4FM",
    )
    info_dmr = models.ForeignKey(
        DimDmr,
        on_delete=models.RESTRICT,
        blank=True,
        null=True,
        verbose_name="info - DMR",
    )
    info_tetra = models.ForeignKey(
        DimTetra,
        on_delete=models.RESTRICT,
        blank=True,
        null=True,
        verbose_name="info - TETRA",
    )

    # Info
    info_holder = models.ForeignKey(
        Association,
        on_delete=models.RESTRICT,
        blank=True,
        null=True,
        verbose_name="info - holder",
    )
    info_location = models.ForeignKey(
        DimLocation,
        on_delete=models.RESTRICT,
        verbose_name="info - location",
    )

    @computed(
        ArrayField(
            models.CharField(
                max_length=64,
                verbose_name="mode",
                choices=MODE_CHOICES,
                default=[],
            ),
            size=4,
        ),
        depends=[
            ("self", ["info_fm", "info_dstar", "info_fusion", "info_dmr", "info_tetra"])
        ],
    )
    def modes(self) -> list[str]:
        """
        Compute the modes of the repeater based on the availability of the corresponding
        data.
        """
        modes = []
        if self.info_fm is not None:
            modes.append(self.ModeOptions.FM)
        if self.info_dstar is not None:
            modes.append(self.ModeOptions.DSTAR)
        if self.info_fusion is not None:
            modes.append(self.ModeOptions.FUSION)
        if self.info_dmr is not None:
            modes.append(self.ModeOptions.DMR)
        if self.info_tetra is not None:
            modes.append(self.ModeOptions.TETRA)
        return modes

    def __str__(self) -> str:
        return str(self.callsign)

    class Meta:
        verbose_name = "repeater"
        verbose_name_plural = "repeaters"

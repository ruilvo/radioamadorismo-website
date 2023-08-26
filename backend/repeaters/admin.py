"""
Admin interface for the repeaters app.
"""

from django.contrib import admin

from django_admin_geomap import ModelAdmin as GeoModelAdmin

from repeaters.models import (
    DimRf,
    DimFm,
    DimDstar,
    DimFusion,
    DimDmrTg,
    DimDmr,
    DimTetra,
    DimLocation,
    FactRepeater,
)


class FactRepeaterInline(admin.StackedInline):
    model = FactRepeater


@admin.register(DimRf)
class DimRfAdmin(admin.ModelAdmin):
    """
    Admin interface for the DimRf model.
    """

    save_as = True
    save_on_top = True
    inlines = (FactRepeaterInline,)
    list_display = (
        "id",
        "channel",
        "tx_mhz",
        "rx_mhz",
        "shift_mhz",
        "band",
        "mode",
    )
    search_fields = (
        "id",
        "channel",
        "tx_mhz",
        "rx_mhz",
        "shift_mhz",
        "band",
        "mode",
    )
    ordering = (
        "mode",
        "band",
        "tx_mhz",
        "rx_mhz",
        "channel",
        "shift_mhz",
        "id",
    )


@admin.register(DimFm)
class DimFmAdmin(admin.ModelAdmin):
    """
    Admin interface for the DimFm model.
    """

    save_as = True
    save_on_top = True
    inlines = (FactRepeaterInline,)
    list_display = (
        "id",
        "bandwidth",
        "modulation",
        "tone",
    )
    search_fields = (
        "id",
        "bandwidth",
        "modulation",
        "tone",
    )
    ordering = (
        "bandwidth",
        "modulation",
        "tone",
        "id",
    )


@admin.register(DimDstar)
class DimDstarTriggerMigrationAdmin(admin.ModelAdmin):
    """
    Admin interface for the DimDstar model.
    """

    save_as = True
    save_on_top = True
    inlines = (FactRepeaterInline,)
    list_display = (
        "id",
        "gateway",
        "reflector",
    )
    search_fields = (
        "id",
        "gateway",
        "reflector",
    )
    ordering = (
        "gateway",
        "reflector",
        "id",
    )


@admin.register(DimFusion)
class DimFusionAdmin(admin.ModelAdmin):
    """
    Admin interface for the DimFusion model.
    """

    save_as = True
    save_on_top = True
    inlines = (FactRepeaterInline,)
    list_display = (
        "id",
        "wiresx",
        "room_id",
    )
    search_fields = (
        "id",
        "wiresx",
        "room_id",
    )
    ordering = (
        "wiresx",
        "room_id",
        "id",
    )


@admin.register(DimDmrTg)
class DimDmrTgAdmin(admin.ModelAdmin):
    """
    Admin interface for the DimDmrTg model.
    """

    save_as = True
    save_on_top = True
    list_display = (
        "id",
        "call_mode",
        "name",
    )
    search_fields = (
        "call_mode",
        "id",
        "name",
    )
    ordering = (
        "call_mode",
        "id",
        "name",
    )


@admin.register(DimDmr)
class DimDmrAdmin(admin.ModelAdmin):
    """
    Admin interface for the DimDmr model.
    """

    save_as = True
    save_on_top = True
    inlines = (FactRepeaterInline,)
    list_display = (
        "get_id",
        "get_name",
    )
    search_fields = ("__str__",)

    @admin.display(description="ID")
    def get_id(self, obj: DimDmr):
        return obj.tg.id

    @admin.display(description="Name")
    def get_name(self, obj: DimDmr):
        return obj.tg.name


@admin.register(DimTetra)
class DimTetraAdmin(admin.ModelAdmin):
    """
    Admin interface for the DimTetra model.
    """

    save_as = True
    save_on_top = True
    inlines = (FactRepeaterInline,)
    list_display = (
        "id",
        "mcc",
        "mnc",
    )
    search_fields = (
        "id",
        "mcc",
        "mnc",
    )
    ordering = (
        "mcc",
        "mnc",
        "id",
    )


@admin.register(DimLocation)
class DimLocationAdmin(GeoModelAdmin):
    """
    Admin interface for the DimLocation model.
    """

    geomap_field_longitude = "id_longitude"
    geomap_field_latitude = "id_latitude"

    save_as = True
    save_on_top = True
    inlines = (FactRepeaterInline,)
    list_display = (
        "id",
        "place",
        "region",
        "qth_loc",
        "latitude",
        "longitude",
    )
    search_fields = (
        "id",
        "place",
        "region",
        "qth_loc",
        "latitude",
        "longitude",
    )
    ordering = (
        "region",
        "qth_loc",
        "latitude",
        "longitude",
        "place",
        "id",
    )


@admin.register(FactRepeater)
class FactRepeaterAdmin(GeoModelAdmin):
    """
    Admin interface for the FactRepeater model.
    """

    save_as = True
    save_on_top = True
    autocomplete_fields = (
        "info_rf",
        "info_fm",
        "info_dstar",
        "info_fusion",
        "info_dmr",
        "info_tetra",
        "info_holder",
        "info_location",
    )
    list_display = (
        "id",
        "callsign",
        "modes",
        "info_holder",
    )
    search_fields = (
        "id",
        "callsign",
        "info_holder__abrv",
    )
    ordering = (
        "info_holder",
        "callsign",
        "id",
    )

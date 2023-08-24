"""
Admin interface for the repeaters app.
"""

from django.contrib import admin

from django_admin_geomap import ModelAdmin as GeoModelAdmin

from repeaters.models import (
    DimRf,
    DimFm,
    DimDStar,
    DimFusion,
    DimDmrTg,
    DimDmr,
    DimHolder,
    DimLocation,
    FactRepeater,
)


class FactRepeaterInline(admin.StackedInline):
    model = FactRepeater


class DimRfAdmin(admin.ModelAdmin):
    """
    Admin interface for the DimRf model.
    """

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


admin.site.register(DimRf, DimRfAdmin)


class DimFmAdmin(admin.ModelAdmin):
    """
    Admin interface for the DimFm model.
    """

    inlines = (FactRepeaterInline,)
    list_display = (
        "bandwidth",
        "modulation",
        "tone",
    )
    search_fields = (
        "bandwidth",
        "modulation",
        "tone",
    )
    ordering = (
        "bandwidth",
        "modulation",
        "tone",
    )


admin.site.register(DimFm, DimFmAdmin)


class DimDStarAdmin(admin.ModelAdmin):
    """
    Admin interface for the DimDStar model.
    """

    inlines = (FactRepeaterInline,)
    list_display = (
        "modulation",
        "gateway",
        "reflector",
    )
    search_fields = (
        "modulation",
        "gateway",
        "reflector",
    )
    ordering = (
        "modulation",
        "gateway",
        "reflector",
    )


admin.site.register(DimDStar, DimDStarAdmin)


class DimFusionAdmin(admin.ModelAdmin):
    """
    Admin interface for the DimFusion model.
    """

    inlines = (FactRepeaterInline,)
    list_display = (
        "modulation",
        "wiresx",
        "room_id",
    )
    search_fields = (
        "modulation",
        "wiresx",
        "room_id",
    )
    ordering = (
        "modulation",
        "wiresx",
        "room_id",
    )


admin.site.register(DimFusion, DimFusionAdmin)


class DimDmrTgAdmin(admin.ModelAdmin):
    """
    Admin interface for the DimDmrTg model.
    """

    list_display = (
        "call_mode",
        "id",
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


admin.site.register(DimDmrTg, DimDmrTgAdmin)


class DimDmrAdmin(admin.ModelAdmin):
    """
    Admin interface for the DimDmr model.
    """

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


admin.site.register(DimDmr, DimDmrAdmin)


class DimHolderAdmin(admin.ModelAdmin):
    """
    Admin interface for the DimHolder model.
    """

    inlines = (FactRepeaterInline,)
    list_display = (
        "id",
        "abrv",
        "name",
    )
    search_fields = (
        "id",
        "abrv",
        "name",
    )
    ordering = (
        "abrv",
        "name",
        "id",
    )


admin.site.register(DimHolder, DimHolderAdmin)


class DimLocationAdmin(GeoModelAdmin):
    """
    Admin interface for the DimLocation model.
    """

    geomap_field_longitude = "id_longitude"
    geomap_field_latitude = "id_latitude"

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


admin.site.register(DimLocation, DimLocationAdmin)


class FactRepeaterAdmin(admin.ModelAdmin):
    """
    Admin interface for the FactRepeater model.
    """

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


admin.site.register(FactRepeater, FactRepeaterAdmin)

"""
Admin interface for the repeaters app.
"""

from django.contrib import admin

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


class DimRfAdmin(admin.ModelAdmin):
    """
    Admin interface for the DimRf model.
    """

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
        "id",
        "channel",
        "tx_mhz",
        "rx_mhz",
        "shift_mhz",
        "band",
        "mode",
    )


admin.site.register(DimRf, DimRfAdmin)

admin.site.register(DimFm)
admin.site.register(DimDStar)
admin.site.register(DimFusion)
admin.site.register(DimDmrTg)
admin.site.register(DimDmr)


class DimHolderAdmin(admin.ModelAdmin):
    """
    Admin interface for the DimHolder model.
    """

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
        "id",
        "abrv",
        "name",
    )


admin.site.register(DimHolder, DimHolderAdmin)


class DimLocationAdmin(admin.ModelAdmin):
    """
    Admin interface for the DimLocation model.
    """

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
        "id",
        "place",
        "region",
        "qth_loc",
        "latitude",
        "longitude",
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
        "id",
        "callsign",
        "info_holder",
    )


admin.site.register(FactRepeater, FactRepeaterAdmin)

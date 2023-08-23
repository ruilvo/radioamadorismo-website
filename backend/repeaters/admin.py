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

admin.site.register(DimRf)
admin.site.register(DimFm)
admin.site.register(DimDStar)
admin.site.register(DimFusion)
admin.site.register(DimDmrTg)
admin.site.register(DimDmr)
admin.site.register(DimHolder)
admin.site.register(DimLocation)


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

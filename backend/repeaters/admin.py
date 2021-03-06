from django.contrib import admin

from repeaters.models import (
    DimHalfDuplex,
    DimSimplex,
    DimFm,
    DimDStar,
    DimFusion,
    DimDmrTg,
    DimDmr,
    DimHolder,
    DimLocation,
    FactRepeater,
)

admin.site.register(DimHalfDuplex)
admin.site.register(DimSimplex)
admin.site.register(DimFm)
admin.site.register(DimDStar)
admin.site.register(DimFusion)
admin.site.register(DimDmrTg)
admin.site.register(DimDmr)
admin.site.register(DimHolder)
admin.site.register(DimLocation)
admin.site.register(FactRepeater)

from django.contrib import admin

from .models import (
    DimHalfDuplex,
    DimSimplex,
    DimFm,
    DimDStar,
    DimFusion,
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
admin.site.register(DimDmr)
admin.site.register(DimHolder)
admin.site.register(DimLocation)
admin.site.register(FactRepeater)

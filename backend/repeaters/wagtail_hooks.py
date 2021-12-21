from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    ModelAdminGroup,
    modeladmin_register,
)
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


class DimHalfDuplexAdmin(ModelAdmin):
    model = DimHalfDuplex


class DimSimplexAdmin(ModelAdmin):
    model = DimSimplex


class DimFmAdmin(ModelAdmin):
    model = DimFm


class DimDStarAdmin(ModelAdmin):
    model = DimDStar


class DimFusionAdmin(ModelAdmin):
    model = DimFusion


class DimDmrAdmin(ModelAdmin):
    model = DimDmr


class DimHolderAdmin(ModelAdmin):
    model = DimHolder


class DimLocationAdmin(ModelAdmin):
    model = DimLocation


class FactRepeaterAdmin(ModelAdmin):
    model = FactRepeater


class RepeatersGroup(ModelAdminGroup):
    menu_label = "Repeaters"
    items = (
        DimHalfDuplexAdmin,
        DimSimplexAdmin,
        DimFmAdmin,
        DimDStarAdmin,
        DimFusionAdmin,
        DimDmrAdmin,
        DimHolderAdmin,
        DimLocationAdmin,
        FactRepeaterAdmin,
    )


modeladmin_register(RepeatersGroup)

from rest_framework.routers import SimpleRouter

from repeaters.api.views import (
    DimHalfDuplexViewSet,
    DimSimplexViewSet,
    DimFmViewSet,
    DimDStarViewSet,
    DimFusionViewSet,
    DimDmrTgViewSet,
    DimDmrViewSet,
    DimHolderViewSet,
    DimLocationViewSet,
    FactRepeaterViewSet,
)


router = SimpleRouter()
router.register("fact-repeater", FactRepeaterViewSet, basename="fact-repeater")
router.register("dim-half-duplex", DimHalfDuplexViewSet, basename="dim-half-duplex")
router.register("dim-simplex", DimSimplexViewSet, basename="dim-simplex")
router.register("dim-fm", DimFmViewSet, basename="dim-fm")
router.register("dim-dstar", DimDStarViewSet, basename="dim-dstar")
router.register("dim-fusion", DimFusionViewSet, basename="dim-fusion")
router.register("dim-dmr-tg", DimDmrTgViewSet, basename="dim-dmr-tg")
router.register("dim-dmr", DimDmrViewSet, basename="dim-dmr")
router.register("dim-holder", DimHolderViewSet, basename="dim-holder")
router.register("dim-location", DimLocationViewSet, basename="dim-location")

urlpatterns = router.urls

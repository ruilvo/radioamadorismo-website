"""
Define the URL routes for the repeaters API.
"""

from rest_framework.routers import SimpleRouter

from repeaters.api.views import (
    DimRfViewSet,
    DimFmViewSet,
    DimDStarViewSet,
    DimFusionViewSet,
    DimDmrTgViewSet,
    DimDmrViewSet,
    DimTetraViewSet,
    DimLocationViewSet,
    FactRepeaterViewSet,
)


router = SimpleRouter()
router.register("fact-repeater", FactRepeaterViewSet, basename="fact-repeater")
router.register("dim-rf", DimRfViewSet, basename="dim-rf")
router.register("dim-fm", DimFmViewSet, basename="dim-fm")
router.register("dim-dstar", DimDStarViewSet, basename="dim-dstar")
router.register("dim-fusion", DimFusionViewSet, basename="dim-fusion")
router.register("dim-dmr-tg", DimDmrTgViewSet, basename="dim-dmr-tg")
router.register("dim-dmr", DimDmrViewSet, basename="dim-dmr")
router.register("dim-tetra", DimTetraViewSet, basename="dim-tetra")
router.register("dim-location", DimLocationViewSet, basename="dim-location")

urlpatterns = router.urls

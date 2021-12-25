from rest_framework.routers import SimpleRouter

from .views import WagtailMediaViewSet, WagtailEmbedViewSet


router = SimpleRouter()
router.register("media", WagtailMediaViewSet, basename="wagtailmediaviewset")
router.register("embed", WagtailEmbedViewSet, basename="wagtailembedviewset")

urlpatterns = router.urls

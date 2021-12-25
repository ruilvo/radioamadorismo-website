from rest_framework.routers import SimpleRouter

from .views import WagtailMediaViewSet


router = SimpleRouter()
router.register("", WagtailMediaViewSet, basename="wagtailmediautils")

urlpatterns = router.urls

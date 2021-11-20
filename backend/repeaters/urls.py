from rest_framework.routers import SimpleRouter
from .views import FactRepeaterViewSet

router = SimpleRouter()
router.register("", FactRepeaterViewSet, basename="repeaters")

urlpatterns = router.urls

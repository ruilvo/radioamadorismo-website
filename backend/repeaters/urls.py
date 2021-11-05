from rest_framework.routers import SimpleRouter
from .views import FactRepeaterViewSet

router = SimpleRouter()
router.register("", FactRepeaterViewSet, basename="posts")

urlpatterns = router.urls

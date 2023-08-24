"""
Define the URL routes for the associations API.
"""

from rest_framework.routers import SimpleRouter

from associations.api.views import AssociationViewSet

router = SimpleRouter()
router.register("association", AssociationViewSet, basename="association")

urlpatterns = router.urls

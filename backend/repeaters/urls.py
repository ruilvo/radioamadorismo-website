from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework.schemas import get_schema_view
from .views import FactRepeaterViewSet

router = SimpleRouter()
router.register("", FactRepeaterViewSet, basename="repeaters")

urlpatterns = router.urls

urlpatterns += [
    path(
        "openapi",
        get_schema_view(
            title="Repetidores API",
            description="API para repetidores de radioamadorismo",
            version="1.0.0",
            urlconf="repeaters.urls",
        ),
        name="openapi-schema",
    ),
]

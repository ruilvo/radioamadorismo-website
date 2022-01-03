from django.urls import path, include

from .views import chirp_view

urlpatterns = [
    path(
        "export/",
        include(
            [
                path("chirp/", chirp_view),
            ]
        ),
    )
]

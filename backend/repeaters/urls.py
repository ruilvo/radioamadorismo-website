from django.urls import path, include

from .views import (
    d878uvii_tgs_view,
    d878uvii_rgs_view,
)

urlpatterns = [
    path(
        "export/",
        include(
            [
                path(
                    "d878uvii/",
                    include(
                        [
                            path("tgs/", d878uvii_tgs_view, name="d878uvii_tgs_view"),
                            path("rgs/", d878uvii_rgs_view, name="d878uvii_rgs_view"),
                        ]
                    ),
                ),
            ]
        ),
    )
]

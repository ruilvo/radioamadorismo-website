from django.urls import path, include

from .views import (
    d878uvii_tgs_view,
    d878uvii_rgs_view,
    d878uvii_channels_view,
    d878uvii_zones_view,
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
                            path(
                                "channel/",
                                d878uvii_channels_view,
                                name="d878uvii_channels_view",
                            ),
                            path(
                                "zone/", d878uvii_zones_view, name="d878uvii_zones_view"
                            ),
                        ]
                    ),
                ),
            ]
        ),
    )
]

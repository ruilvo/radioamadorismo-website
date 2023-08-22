"""
Django URLs for the repeaters app
"""

from django.urls import path, include

from repeaters.views import (
    d878uvii_tgs_view,
    d878uvii_rgs_view,
    d878uvii_channels_view,
    d878uvii_zones_view,
    d878uvii_codeplug_view,
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
                            path(
                                "talk-groups/",
                                d878uvii_tgs_view,
                                name="d878uvii_tgs_view",
                            ),
                            path(
                                "receive-group-call-list/",
                                d878uvii_rgs_view,
                                name="d878uvii_rgs_view",
                            ),
                            path(
                                "channel/",
                                d878uvii_channels_view,
                                name="d878uvii_channels_view",
                            ),
                            path(
                                "zone/", d878uvii_zones_view, name="d878uvii_zones_view"
                            ),
                            path(
                                "codeplug/",
                                d878uvii_codeplug_view,
                                name="d878uvii_codeplug_view",
                            ),
                        ]
                    ),
                ),
            ]
        ),
    )
]

"""
Django URLs for the repeaters app
"""

from django.urls import path, include

from repeaters.views import (
    chirp_csv_view,
    anytone_d878uviip_view,
)

urlpatterns = [
    path(
        "export/",
        include(
            [
                path(
                    "chirp/",
                    chirp_csv_view,
                    name="chirp_csv_view",
                ),
                path(
                    "anytone_d878uviip/",
                    anytone_d878uviip_view,
                    name="anytone_d878uviip_view",
                ),
            ]
        ),
    )
]

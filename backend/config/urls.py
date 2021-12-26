"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    # Django
    path("admin/", admin.site.urls),
    # API
    path(
        "api/",
        include(
            [
                # Auth
                path(
                    "auth/",
                    include(
                        [
                            path(
                                "drf-auth/",
                                include("rest_framework.urls"),
                                name="drf-auth",
                            ),
                            path(
                                "dj-rest-auth/",
                                include("dj_rest_auth.urls"),
                                name="dj-rest-auth",
                            ),
                        ]
                    ),
                ),
                # Schema
                path("schema/", SpectacularAPIView.as_view(), name="schema"),
                path(
                    "reference/",
                    include(
                        [
                            path(
                                "swagger-ui/",
                                SpectacularSwaggerView.as_view(url_name="schema"),
                                name="swagger-ui",
                            ),
                            path(
                                "redoc/",
                                SpectacularRedocView.as_view(url_name="schema"),
                                name="redoc",
                            ),
                        ]
                    ),
                ),
                # Local
                path(
                    "v1/",
                    include(
                        [
                            path(
                                "repeaters/",
                                include("repeaters.urls"),
                                name="repeaters",
                            ),
                        ]
                    ),
                ),
            ],
        ),
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

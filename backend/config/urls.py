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

from rest_framework.schemas import get_schema_view

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from .wagtail_api import api_router as wagtail_api_router

authpatterns = [
    path("drf-auth/", include("rest_framework.urls")),
    path("dj-rest-auth/", include("dj_rest_auth.urls")),
]

apipatterns = [
    # Local
    path("repeaters/", include("repeaters.urls")),
]

schemapatterns = [
    path(
        "api/openapi/",
        get_schema_view(
            title="Portal do Radioamadorismo: API",
            version="1.0.0",
        ),
        name="openapi-schema",
    ),
]

urlpatterns = [
    # Django
    path("admin/", admin.site.urls),
    # Wagtail
    path("cms/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("pages/", include(wagtail_urls)),
    # Wagtail API
    path("api/v2/wagtail/", wagtail_api_router.urls),
    # Auth
    path("api/auth/", include(authpatterns)),
    # APIs
    path("api/v1/", include(apipatterns)),
    # Schema
    path("", include(schemapatterns)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

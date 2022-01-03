from django.urls import path

from .api_views import get_passcode

urlpatterns = [
    path("passcode-generator/", get_passcode),
]

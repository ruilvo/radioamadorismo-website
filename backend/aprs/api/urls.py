from django.urls import path

from aprs.api.views import get_passcode

urlpatterns = [
    path("passcode-generator/", get_passcode),
]

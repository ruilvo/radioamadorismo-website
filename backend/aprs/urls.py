from django.urls import path

from .views import get_passcode

urlpatterns = [
    path("passcode-generator/", get_passcode),
]

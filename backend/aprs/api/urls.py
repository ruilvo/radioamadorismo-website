from django.urls import path

from aprs.api.views import PasscodeView

urlpatterns = [
    path("passcode-generator/", PasscodeView.as_view()),
]

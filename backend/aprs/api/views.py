"""
Views for the APRS API
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from drf_spectacular.utils import extend_schema

from aprs.api.serializers import CallsignSerializer, PasscodeSerializer
from aprs.vendor.passcode import passcode_generator


class PasscodeView(APIView):
    """
    View to get the APRS passcode from a callsign
    """

    permission_classes = [
        AllowAny,
    ]

    serializer_class = CallsignSerializer

    @extend_schema(responses=PasscodeSerializer)
    def post(self, request):
        """
        Get the APRS passcode from a callsign
        """
        serializer = CallsignSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        callsign = serializer.validated_data["callsign"]
        passcode = passcode_generator(callsign)

        passcode_serializer = PasscodeSerializer(data={"passcode": passcode})
        passcode_serializer.is_valid(raise_exception=True)

        # The serializer isn't passed here directly because otherwise DRF's browsable API
        # will create a POST form for the PasscodeSerializer, instead of the
        # CallsignSerializer. It is used in the lines above, instead of passing a
        # dictionary here directly as a form of validation.
        return Response(passcode_serializer.validated_data)

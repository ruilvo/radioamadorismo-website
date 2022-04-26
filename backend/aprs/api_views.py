from rest_framework.decorators import api_view, permission_classes
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    OpenApiResponse,
    inline_serializer,
)

from .passcode_generator import passcode_generator


@extend_schema(
    parameters=[
        OpenApiParameter(name="callsign", required=True, type=str),
    ],
    description="Get an APRS-IS passcode for a given callsign",
    responses={
        200: inline_serializer(
            name="PasscodeResponse",
            fields={
                "passcode": serializers.CharField(),
            },
        ),
        400: OpenApiResponse(description="Missing callsign"),
    },
)
@api_view(["POST"])
@permission_classes([AllowAny])
def get_passcode(request):
    callsign = request.data.get("callsign", None)
    if callsign is None:
        return Response(
            {"error": "Missing callsign"}, status=status.HTTP_400_BAD_REQUEST
        )
    return Response({"passcode": passcode_generator(callsign)})

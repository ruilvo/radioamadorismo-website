from rest_framework import response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse

from .passcode_generator import passcode_generator


@extend_schema(
    parameters=[
        OpenApiParameter(name="callsign", required=True, type=str),
    ],
    description="Get an APRS-IS passcode for a given callsign",
)
@api_view(["POST"])
@permission_classes([AllowAny])
def get_passcode(request):
    callsign = request.data.get("callsign", None)
    if callsign is None:
        raise Response(
            {"error": "Missing callsign"}, status=status.HTTP_400_BAD_REQUEST
        )
    return Response({"passcode": passcode_generator(callsign)})

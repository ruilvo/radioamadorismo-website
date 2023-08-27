"""
Define the ViewSets for the repeaters API.
"""

from rest_framework import status, viewsets
from rest_framework.response import Response

from repeaters.models import (
    DimRf,
    DimFm,
    DimDstar,
    DimFusion,
    DimDmrTg,
    DimDmr,
    DimTetra,
    DimLocation,
    FactRepeater,
)
from repeaters.api.serializers import (
    DimRfSerializer,
    DimFmSerializer,
    DimDstarSerializer,
    DimFusionSerializer,
    DimDmrTgSerializer,
    DimDmrSerializer,
    DimTetraSerializer,
    DimLocationSerializer,
    FactRepeaterSerializer,
)

from repeaters.api.filters import (
    DimRfFilter,
    DimLocationFilter,
    FactRepeaterFilter,
)


class NestedWritableModelViewSet(  # pylint: disable=too-many-ancestors
    viewsets.ModelViewSet
):
    def create(self, request, *args, **kwargs):
        """
        Create a list of model instances if a list is provided or a
        single model instance otherwise.
        """
        data = request.data
        to_return = None
        headers = {}
        if isinstance(data, list):
            to_return = [self._create_one_instance(item).data for item in data]
        else:
            serializer = self._create_one_instance(data)
            to_return = serializer.data
            headers = self.get_success_headers(to_return)
        return Response(to_return, status=status.HTTP_201_CREATED, headers=headers)

    def _create_one_instance(self, item):
        """
        Helper method to create a single model instance.
        """
        serializer = self.get_serializer(data=item)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return serializer


class FactRepeaterViewSet(  # pylint: disable=too-many-ancestors
    NestedWritableModelViewSet
):
    """
    ViewSet for FactRepeater model.
    """

    queryset = FactRepeater.objects.all()
    serializer_class = FactRepeaterSerializer

    filterset_class = FactRepeaterFilter

    ordering_fields = (
        "callsign",
        "pwr_w",
        "status",
        "info_rf__tx_mhz",
        "info_rf__rx_mhz",
        "info_rf__channel",
        "info_rf__band",
        "info_rf__mode",
        "info_rf__shift_mhz",
        "info_fm__modulation",
        "info_fm__tone",
        "info_fm__bandwidth",
        "info_dstar__gateway",
        "info_dstar__reflector",
        "info_fusion__wiresx",
        "info_fusion__room_id",
        "info_dmr__tg__id",
        "info_dmr__tg__name",
        "info_dmr__tg__call_mode",
        "info_dmr__color_code",
        "info_tetra__mcc",
        "info_tetra__mnc",
        "info_location__latitude",
        "info_location__longitude",
        "info_location__region",
        "info_location__place",
        "info_location__qth_loc",
    )

    ordering = (  # Default ordering
        "info_location__region",
        "-info_location__latitude",
    )


class DimRfViewSet(NestedWritableModelViewSet):  # pylint: disable=too-many-ancestors
    """
    ViewSet for DimRf model.
    """

    queryset = DimRf.objects.all()
    serializer_class = DimRfSerializer
    filterset_class = DimRfFilter
    ordering_fields = (
        "tx_mhz",
        "rx_mhz",
        "channel",
        "band",
        "mode",
        "shift_mhz",
    )


class DimFmViewSet(NestedWritableModelViewSet):  # pylint: disable=too-many-ancestors
    """
    ViewSet for DimFm model.
    """

    queryset = DimFm.objects.all()
    serializer_class = DimFmSerializer
    ordering_fields = (
        "modulation",
        "tone",
        "bandwidth",
    )


class DimDstarViewSet(NestedWritableModelViewSet):  # pylint: disable=too-many-ancestors
    """
    ViewSet for DimDstar model.
    """

    queryset = DimDstar.objects.all()
    serializer_class = DimDstarSerializer
    ordering_fields = (
        "gateway",
        "reflector",
    )


class DimFusionViewSet(  # pylint: disable=too-many-ancestors
    NestedWritableModelViewSet
):
    """
    ViewSet for DimFusion model.
    """

    queryset = DimFusion.objects.all()
    serializer_class = DimFusionSerializer
    ordering_fields = (
        "wiresx",
        "room_id",
    )


class DimDmrTgViewSet(NestedWritableModelViewSet):  # pylint: disable=too-many-ancestors
    """
    ViewSet for DimDmrTg model.
    """

    queryset = DimDmrTg.objects.all()
    serializer_class = DimDmrTgSerializer
    ordering_fields = (
        "id",
        "name",
        "call_mode",
    )


class DimDmrViewSet(NestedWritableModelViewSet):  # pylint: disable=too-many-ancestors
    """
    ViewSet for DimDmr model.
    """

    queryset = DimDmr.objects.all()
    serializer_class = DimDmrSerializer
    ordering_fields = (
        "tg__id",
        "tg__name",
        "tg__call_mode",
        "color_code",
    )


class DimTetraViewSet(NestedWritableModelViewSet):  # pylint: disable=too-many-ancestors
    """
    ViewSet for DimTetra model.
    """

    queryset = DimTetra.objects.all()
    serializer_class = DimTetraSerializer
    ordering_fields = (
        "mcc",
        "mnc",
    )


class DimLocationViewSet(  # pylint: disable=too-many-ancestors
    NestedWritableModelViewSet
):
    """
    ViewSet for DimLocation model.
    """

    queryset = DimLocation.objects.all()
    serializer_class = DimLocationSerializer
    filterset_class = DimLocationFilter
    ordering_fields = (
        "latitude",
        "longitude",
        "region",
        "place",
        "qth_loc",
    )

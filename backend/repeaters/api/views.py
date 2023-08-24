"""
Define the ViewSets for the repeaters API.
"""

from rest_framework import status, viewsets
from rest_framework.response import Response

from repeaters.models import (
    DimRf,
    DimFm,
    DimDStar,
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
    DimDStarSerializer,
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


class DimRfViewSet(NestedWritableModelViewSet):  # pylint: disable=too-many-ancestors
    """
    ViewSet for DimRf model.
    """

    queryset = DimRf.objects.all()
    serializer_class = DimRfSerializer
    filterset_class = DimRfFilter


class DimFmViewSet(NestedWritableModelViewSet):  # pylint: disable=too-many-ancestors
    """
    ViewSet for DimFm model.
    """

    queryset = DimFm.objects.all()
    serializer_class = DimFmSerializer


class DimDStarViewSet(NestedWritableModelViewSet):  # pylint: disable=too-many-ancestors
    """
    ViewSet for DimDStar model.
    """

    queryset = DimDStar.objects.all()
    serializer_class = DimDStarSerializer


class DimFusionViewSet(  # pylint: disable=too-many-ancestors
    NestedWritableModelViewSet
):
    """
    ViewSet for DimFusion model.
    """

    queryset = DimFusion.objects.all()
    serializer_class = DimFusionSerializer


class DimDmrTgViewSet(NestedWritableModelViewSet):  # pylint: disable=too-many-ancestors
    """
    ViewSet for DimDmrTg model.
    """

    queryset = DimDmrTg.objects.all()
    serializer_class = DimDmrTgSerializer


class DimDmrViewSet(NestedWritableModelViewSet):  # pylint: disable=too-many-ancestors
    """
    ViewSet for DimDmr model.
    """

    queryset = DimDmr.objects.all()
    serializer_class = DimDmrSerializer


class DimTetraViewSet(NestedWritableModelViewSet):  # pylint: disable=too-many-ancestors
    """
    ViewSet for DimTetra model.
    """

    queryset = DimTetra.objects.all()
    serializer_class = DimTetraSerializer


class DimLocationViewSet(  # pylint: disable=too-many-ancestors
    NestedWritableModelViewSet
):
    """
    ViewSet for DimLocation model.
    """

    queryset = DimLocation.objects.all()
    serializer_class = DimLocationSerializer
    filterset_class = DimLocationFilter

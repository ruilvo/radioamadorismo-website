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
    DimHolder,
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
    DimHolderSerializer,
    DimLocationSerializer,
    FactRepeaterSerializer,
)

from repeaters.api.filters import (
    DimRfFilter,
    DimHolderFilter,
    DimLocationFilter,
    FactRepeaterFilter,
)


class FactRepeaterViewSet(viewsets.ModelViewSet):  # pylint: disable=too-many-ancestors
    """
    ViewSet for FactRepeater model.
    """

    queryset = FactRepeater.objects.all()
    serializer_class = FactRepeaterSerializer

    filterset_class = FactRepeaterFilter

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


class DimRfViewSet(viewsets.ModelViewSet):  # pylint: disable=too-many-ancestors
    """
    ViewSet for DimRf model.
    """

    queryset = DimRf.objects.all()
    serializer_class = DimRfSerializer
    filterset_class = DimRfFilter


class DimFmViewSet(viewsets.ModelViewSet):  # pylint: disable=too-many-ancestors
    """
    ViewSet for DimFm model.
    """

    queryset = DimFm.objects.all()
    serializer_class = DimFmSerializer


class DimDStarViewSet(viewsets.ModelViewSet):  # pylint: disable=too-many-ancestors
    """
    ViewSet for DimDStar model.
    """

    queryset = DimDStar.objects.all()
    serializer_class = DimDStarSerializer


class DimFusionViewSet(viewsets.ModelViewSet):  # pylint: disable=too-many-ancestors
    """
    ViewSet for DimFusion model.
    """

    queryset = DimFusion.objects.all()
    serializer_class = DimFusionSerializer


class DimDmrTgViewSet(viewsets.ModelViewSet):  # pylint: disable=too-many-ancestors
    """
    ViewSet for DimDmrTg model.
    """

    queryset = DimDmrTg.objects.all()
    serializer_class = DimDmrTgSerializer


class DimDmrViewSet(viewsets.ModelViewSet):  # pylint: disable=too-many-ancestors
    """
    ViewSet for DimDmr model.
    """

    queryset = DimDmr.objects.all()
    serializer_class = DimDmrSerializer


class DimHolderViewSet(viewsets.ModelViewSet):  # pylint: disable=too-many-ancestors
    """
    ViewSet for DimHolder model.
    """

    queryset = DimHolder.objects.all()
    serializer_class = DimHolderSerializer
    filterset_class = DimHolderFilter


class DimLocationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for DimLocation model.
    """

    queryset = DimLocation.objects.all()
    serializer_class = DimLocationSerializer
    filterset_class = DimLocationFilter

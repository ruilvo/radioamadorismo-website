from rest_framework import status, viewsets
from rest_framework.response import Response

from repeaters.models import (
    DimHalfDuplex,
    DimSimplex,
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
    DimHalfDuplexSerializer,
    DimSimplexSerializer,
    DimFmSerializer,
    DimDStarSerializer,
    DimFusionSerializer,
    DimDmrTgSerializer,
    DimDmrSerializer,
    DimHolderSerializer,
    DimLocationSerializer,
    FactRepeaterSerializer,
)

from repeaters.api.filters import FactRepeaterFilter


class FactRepeaterViewSet(viewsets.ModelViewSet):
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
        serializer = self.get_serializer(data=item)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return serializer


class DimHalfDuplexViewSet(viewsets.ModelViewSet):
    queryset = DimHalfDuplex.objects.all()
    serializer_class = DimHalfDuplexSerializer


class DimSimplexViewSet(viewsets.ModelViewSet):
    queryset = DimSimplex.objects.all()
    serializer_class = DimSimplexSerializer


class DimFmViewSet(viewsets.ModelViewSet):
    queryset = DimFm.objects.all()
    serializer_class = DimFmSerializer


class DimDStarViewSet(viewsets.ModelViewSet):
    queryset = DimDStar.objects.all()
    serializer_class = DimDStarSerializer


class DimFusionViewSet(viewsets.ModelViewSet):
    queryset = DimFusion.objects.all()
    serializer_class = DimFusionSerializer


class DimDmrTgViewSet(viewsets.ModelViewSet):
    queryset = DimDmrTg.objects.all()
    serializer_class = DimDmrTgSerializer


class DimDmrViewSet(viewsets.ModelViewSet):
    queryset = DimDmr.objects.all()
    serializer_class = DimDmrSerializer


class DimHolderViewSet(viewsets.ModelViewSet):
    queryset = DimHolder.objects.all()
    serializer_class = DimHolderSerializer


class DimLocationViewSet(viewsets.ModelViewSet):
    queryset = DimLocation.objects.all()
    serializer_class = DimLocationSerializer

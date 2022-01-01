from rest_framework import viewsets

from .models import (
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
from .serializers import (
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

from .filters import FactRepeaterFilterDRF


class FactRepeaterViewSet(viewsets.ModelViewSet):

    queryset = FactRepeater.objects.all()
    serializer_class = FactRepeaterSerializer

    filterset_class = FactRepeaterFilterDRF


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

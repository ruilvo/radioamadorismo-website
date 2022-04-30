from rest_framework import status, viewsets
from rest_framework.response import Response

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

from .filters import FactRepeaterFilterDrf


class FactRepeaterViewSet(viewsets.ModelViewSet):

    queryset = FactRepeater.objects.all()
    serializer_class = FactRepeaterSerializer

    filterset_class = FactRepeaterFilterDrf

    def create(self, request, *args, **kwargs):
        """
        Create a list of model instances if a list is provided or a
        single model instance otherwise.
        """
        data = request.data
        if isinstance(data, list):
            to_return = []
            for item in data:
                serializer = self.get_serializer(data=item)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                to_return.append(serializer.data)
            return Response(to_return, status=status.HTTP_201_CREATED, headers={})
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


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

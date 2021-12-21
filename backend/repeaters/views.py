from rest_framework import viewsets
from .models import FactRepeater
from .serializers import FactRepeaterSerializer

from .filters import FactRepeaterFilter


class FactRepeaterViewSet(viewsets.ModelViewSet):

    queryset = FactRepeater.objects.all()
    serializer_class = FactRepeaterSerializer

    filterset_class = FactRepeaterFilter

from rest_framework import viewsets
from .models import FactRepeater
from .serializers import FactRepeaterSerializer


class FactRepeaterViewSet(viewsets.ModelViewSet):
    queryset = FactRepeater.objects.all()
    serializer_class = FactRepeaterSerializer

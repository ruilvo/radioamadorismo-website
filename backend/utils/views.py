from rest_framework import viewsets

from .serializers import CURRENT_WAGTAIL_MEDIA_MODEL, WagtailMediaSerializer


class WagtailMediaViewSet(viewsets.ModelViewSet):

    queryset = CURRENT_WAGTAIL_MEDIA_MODEL.objects.all()
    serializer_class = WagtailMediaSerializer

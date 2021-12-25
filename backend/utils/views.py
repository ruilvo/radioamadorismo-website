from rest_framework import viewsets

from wagtail.embeds.models import Embed

from .serializers import (
    CURRENT_WAGTAIL_MEDIA_MODEL,
    WagtailMediaSerializer,
    WagtailEmbedSerializer,
)


class WagtailMediaViewSet(viewsets.ModelViewSet):

    queryset = CURRENT_WAGTAIL_MEDIA_MODEL.objects.all()
    serializer_class = WagtailMediaSerializer


class WagtailEmbedViewSet(viewsets.ModelViewSet):

    queryset = Embed.objects.all()
    serializer_class = WagtailEmbedSerializer

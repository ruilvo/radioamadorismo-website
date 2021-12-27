from rest_framework import viewsets

from .models import (
    FactImage,
    FactBlogPost,
)

from .serializers import FactImageSerializer, FactBlogPostSerializer


class FactImageViewSet(viewsets.ModelViewSet):

    queryset = FactImage.objects.all()
    serializer_class = FactImageSerializer


class FactBlogPostViewSet(viewsets.ModelViewSet):

    queryset = FactBlogPost.objects.all()
    serializer_class = FactBlogPostSerializer

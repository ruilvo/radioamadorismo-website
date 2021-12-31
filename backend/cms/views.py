from rest_framework import viewsets

from .models import (
    FactPdf,
    FactImage,
    FactBlogPost,
)

from .serializers import (
    FactPdfSerializer,
    FactImageSerializer,
    FactBlogPostDetailSerializer,
    FactBlogPostListSerializer,
)


class FactPdfViewSet(viewsets.ModelViewSet):

    queryset = FactPdf.objects.all()
    serializer_class = FactPdfSerializer


class FactImageViewSet(viewsets.ModelViewSet):

    queryset = FactImage.objects.all()
    serializer_class = FactImageSerializer


class FactBlogPostViewSet(viewsets.ModelViewSet):

    queryset = FactBlogPost.objects.all()
    serializer_class = FactBlogPostDetailSerializer

    ordering = ["-added"]

    serializer_class_by_action = {
        "retrieve": FactBlogPostDetailSerializer,
        "list": FactBlogPostListSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_class_by_action.get(self.action, self.serializer_class)

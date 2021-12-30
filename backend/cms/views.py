from rest_framework import viewsets

from .models import (
    FactImage,
    FactBlogPost,
)

from .serializers import (
    FactImageSerializer,
    FactBlogPostDetailSerializer,
    FactBlogPostListSerializer,
)


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

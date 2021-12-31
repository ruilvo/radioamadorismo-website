from rest_framework import serializers

from .models import (
    FactPdf,
    FactImage,
    FactBlogPost,
)


class FactPdfSerializer(serializers.ModelSerializer):
    class Meta:
        model = FactPdf
        fields = "__all__"


class FactImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FactImage
        fields = "__all__"


class FactBlogPostDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = FactBlogPost
        fields = "__all__"


class FactBlogPostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = FactBlogPost
        fields = ["id", "title", "added", "intro"]

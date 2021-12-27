from rest_framework import serializers

from .models import (
    FactImage,
    FactBlogPost,
)


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
        fields = ["id", "title", "added"]

from rest_framework import serializers

from .models import FactExamQuestion


class FactExamQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FactExamQuestion
        fields = "__all__"

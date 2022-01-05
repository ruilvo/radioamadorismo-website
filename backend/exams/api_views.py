from rest_framework import viewsets

from .models import FactExamQuestion
from .filters import FactRepeaterFilterDrf
from .serializers import FactExamQuestionSerializer


class FactExamQuestionViewSet(viewsets.ModelViewSet):

    queryset = FactExamQuestion.objects.all()
    serializer_class = FactExamQuestionSerializer

    filterset_class = FactRepeaterFilterDrf

from functools import reduce

import re
from django.db.models import Q
import django_filters as df
from django_filters import rest_framework as df_rf
from django_filters import filters

from .models import FactExamQuestion


class FactExamQuestionFilter:
    category = filters.CharFilter(label="category", method="category_search")

    def category_search(self, queryset, name, value):
        categories = re.findall(r"[\w']+", value)
        [Q(category=c) for c in categories]
        queryset = queryset.filter(
            reduce(lambda x, y: x | y, [Q(category=c) for c in categories])
        )
        return queryset

    class Meta:
        model = FactExamQuestion
        fields = {
            "question": ["exact", "iexact", "icontains"],
        }


class FactRepeaterFilterDrf(FactExamQuestionFilter, df_rf.FilterSet):
    pass


class FactRepeaterFilterView(FactExamQuestionFilter, df.FilterSet):
    pass

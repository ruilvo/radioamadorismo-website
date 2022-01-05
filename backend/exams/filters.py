from functools import reduce

import re
from django.db.models import Q
import django_filters as df
from django_filters import rest_framework as df_rf

from .models import FactExamQuestion


def category_search(queryset, name, value):
    categories = re.findall(r"[\w]+", value)
    queryset_filtered = queryset.filter(
        reduce(lambda x, y: x | y, [Q(category=c) for c in categories])
    )
    return queryset_filtered


automatic_fields = {
    "question": ["exact", "iexact", "icontains"],
}


class FactRepeaterFilterDrf(df_rf.FilterSet):
    category = df_rf.filters.CharFilter(label="category", method=category_search)

    class Meta:
        model = FactExamQuestion
        fields = automatic_fields


class FactRepeaterFilterView(df.FilterSet):
    category = df.filters.CharFilter(label="category", method=category_search)

    class Meta:
        model = FactExamQuestion
        fields = automatic_fields

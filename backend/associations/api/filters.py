"""
Define Django FilterSets for the associations API.
"""

from django.db.models import Q
from django_filters.rest_framework import filters, FilterSet

from associations.models import Association


def association__association_search(queryset, _, value):
    """
    Allows searching for holder data both in the abrv and name fields.
    """
    queryset = queryset.filter(
        Q(abrv__icontains=value) | Q(name__icontains=value)
    ).distinct()
    return queryset


class AssociationFilter(FilterSet):
    """
    Custom FilterSet for Association model.
    """

    holder = filters.CharFilter(
        label="Holder contains", method=association__association_search
    )

    class Meta:
        model = Association
        fields = {
            "abrv": ["iexact", "icontains"],
            "name": ["iexact", "icontains"],
        }

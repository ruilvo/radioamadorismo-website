from django_filters.rest_framework import filters, FilterSet

from repeaters.models import FactRepeater
from repeaters.common.filters import (
    automatic_fields,
    modulation_search,
    holder_search,
    mode_search,
    rf_search,
    freq_mhz_search,
    freq_mhz_search__gte,
    freq_mhz_search__lte,
    region_search,
)


class FactRepeaterFilter(FilterSet):
    # https://stackoverflow.com/a/62878113/5168563
    modulation = filters.CharFilter(label="modulation", method=modulation_search)
    holder = filters.CharFilter(label="holder", method=holder_search)

    mode = filters.CharFilter(label="mode", method=mode_search)
    rf = filters.CharFilter(label="rf", method=rf_search)

    freq_mhz = filters.NumberFilter(label="freq_mhz", method=freq_mhz_search)
    freq_mhz__gte = filters.NumberFilter(
        label="freq_mhz__gte", method=freq_mhz_search__gte
    )
    freq_mhz__lte = filters.NumberFilter(
        label="freq_mhz__lte", method=freq_mhz_search__lte
    )

    region = filters.CharFilter(label="region", method=region_search)

    class Meta:
        model = FactRepeater
        fields = automatic_fields

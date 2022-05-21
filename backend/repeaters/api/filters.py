from django_filters import rest_framework as drf_filters

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


class FactRepeaterFilter(drf_filters.FilterSet):
    # https://stackoverflow.com/a/62878113/5168563
    modulation = drf_filters.filters.CharFilter(
        label="modulation", method=modulation_search
    )
    holder = drf_filters.filters.CharFilter(label="holder", method=holder_search)

    mode = drf_filters.filters.CharFilter(label="mode", method=mode_search)
    rf = drf_filters.filters.CharFilter(label="rf", method=rf_search)

    freq_mhz = drf_filters.filters.NumberFilter(
        label="freq_mhz", method=freq_mhz_search
    )
    freq_mhz__gte = drf_filters.filters.NumberFilter(
        label="freq_mhz__gte", method=freq_mhz_search__gte
    )
    freq_mhz__lte = drf_filters.filters.NumberFilter(
        label="freq_mhz__lte", method=freq_mhz_search__lte
    )

    region = drf_filters.filters.CharFilter(label="region", method=region_search)

    class Meta:
        model = FactRepeater
        fields = automatic_fields

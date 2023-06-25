from django_filters.rest_framework import filters, FilterSet

from repeaters.models import FactRepeater
from repeaters.common.filters import (
    automatic_fields,
    modulation_search,
    holder_search,
    modes_search,
    rf_search,
    freq_mhz_search,
    freq_mhz_search__gte,
    freq_mhz_search__lte,
    region_search,
)


class FactRepeaterFilter(FilterSet):
    # https://stackoverflow.com/a/62878113/5168563
    modulation = filters.CharFilter(label="Modulation", method=modulation_search)
    holder = filters.CharFilter(label="Holder", method=holder_search)

    modes = filters.CharFilter(label="Modes, ','-separated)", method=modes_search)
    rf = filters.CharFilter(
        label="RF (simplex/half-duplex), ','-separated", method=rf_search
    )

    freq_mhz = filters.NumberFilter(label="Frequency (MHz)", method=freq_mhz_search)
    freq_mhz__gte = filters.NumberFilter(
        label="Frequency (MHz) is greater than or equal to ",
        method=freq_mhz_search__gte,
    )
    freq_mhz__lte = filters.NumberFilter(
        label="Frequency (MHz) is less than or equal to ", method=freq_mhz_search__lte
    )

    region = filters.CharFilter(label="Region (,-separated)", method=region_search)

    class Meta:
        model = FactRepeater
        fields = automatic_fields

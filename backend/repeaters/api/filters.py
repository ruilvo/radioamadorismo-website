"""
Define Django FilterSets for the repeaters API.
"""

import re
from functools import reduce

from django.db.models import Q

from django_filters.rest_framework import filters, FilterSet

from repeaters.models import DimRf, DimHolder, DimLocation, FactRepeater

# https://stackoverflow.com/a/62878113/5168563


def dimrf__freq_mhz_search(queryset, _, value):
    """
    Looks for a frequency value both to be equal in tx_mhz and rx_mhz fields.
    """
    queryset = queryset.filter(
        Q(tx_mhz__exact=value) | Q(rx_mhz__exact=value)
    ).distinct()
    return queryset


def dimrf__freq_mhz_search__gte(queryset, _, value):
    """
    Looks for a frequency value to be GTE both in tx_mhz and rx_mhz fields.
    """
    queryset = queryset.filter(Q(tx_mhz__gte=value) | Q(rx_mhz__gte=value)).distinct()
    return queryset


def dimrf__freq_mhz_search__lte(queryset, _, value):
    """
    Looks for a frequency value to be LTE both in tx_mhz and rx_mhz fields.
    """
    queryset = queryset.filter(Q(tx_mhz__lte=value) | Q(rx_mhz__lte=value)).distinct()
    return queryset


def dimrf__bands_seach(queryset, _, value):
    """
    Allows searching for multiple bands at the same time, comma separated.
    """
    band = re.findall(r"[\w]+", value)
    queryset_filtered = queryset.filter(
        reduce(lambda x, y: x | y, [Q(band__icontains=b) for b in band])
    ).distinct()
    return queryset_filtered


def dimrf__modes_search(queryset, _, value):
    """
    Allows searching for multiple modes at the same time, comma separated.
    """
    modes = re.findall(r"[\w]+", value)
    queryset_filtered = queryset.filter(
        reduce(lambda x, y: x | y, [Q(rf__icontains=r) for r in modes])
    ).distinct()
    return queryset_filtered


class DimRfFilter(FilterSet):
    """
    Custom FilterSet for DimRf model.
    """

    freq_mhz = filters.NumberFilter(
        label="Frequency (MHz)", method=dimrf__freq_mhz_search
    )
    freq_mhz__gte = filters.NumberFilter(
        label="Frequency (MHz) is greater than or equal to ",
        method=dimrf__freq_mhz_search__gte,
    )
    freq_mhz__lte = filters.NumberFilter(
        label="Frequency (MHz) is less than or equal to ",
        method=dimrf__freq_mhz_search__lte,
    )
    bands = filters.CharFilter(label="Bands (,-separated)", method=dimrf__bands_seach)
    modes = filters.CharFilter(label="Modes (,-separated)", method=dimrf__modes_search)

    class Meta:
        model = DimRf
        fields = {
            "tx_mhz": ["exact", "gte", "lte"],
            "rx_mhz": ["exact", "gte", "lte"],
            "channel": ["iexact", "icontains"],
            "band": ["iexact"],
            "mode": ["iexact", "icontains"],
        }


def dimholder__holder_search(queryset, _, value):
    """
    Allows searching for holder data both in the abrv and name fields.
    """
    queryset = queryset.filter(
        Q(abrv__icontains=value) | Q(name__icontains=value)
    ).distinct()
    return queryset


class DimHolderFilter(FilterSet):
    """
    Custom FilterSet for DimHolder model.
    """

    holder = filters.CharFilter(
        label="Holder contains", method=dimholder__holder_search
    )

    class Meta:
        model = DimHolder
        fields = {
            "abrv": ["iexact", "icontains"],
            "name": ["iexact", "icontains"],
        }


def dimlocation__region_search(queryset, _, value):
    """
    Allows searching for multiple regions at the same time, comma separated.
    """
    regions = re.findall(r"[\w]+", value)
    queryset_filtered = queryset.filter(
        reduce(lambda x, y: x | y, [Q(region=r) for r in regions])
    ).distinct()
    return queryset_filtered


class DimLocationFilter(FilterSet):
    """
    Custom FilterSet for DimLocation model.
    """

    regions = filters.CharFilter(
        label="Regions (,-separated)", method=dimlocation__region_search
    )

    class Meta:
        model = DimLocation
        fields = {
            "latitude": ["exact", "gte", "lte"],
            "longitude": ["exact", "gte", "lte"],
            "region": ["iexact"],
            "place": ["iexact", "icontains"],
            "qth_loc": ["iexact", "icontains"],
        }


def factrepeater__modes_search(queryset, _, value):
    """
    Allows searching for multiple modes at the same time, comma separated.
    """
    modes = re.findall(r"[\w]+", value)
    allowed_modes = {choice[0] for choice in FactRepeater.MODE_CHOICES}
    query_modes = list({mode.lower() for mode in modes} & allowed_modes)
    return queryset.filter(modes__overlap=query_modes)


class FactRepeaterFilter(FilterSet):
    """
    Custom FilterSet for FactRepeater model.
    """

    modes = filters.CharFilter(
        label="Modes, (,-separated)", method=factrepeater__modes_search
    )

    class Meta:
        model = FactRepeater
        fields = {
            # FactRepeater
            "callsign": ["iexact", "icontains"],
            "notes": ["icontains"],
            "pwr_w": ["exact", "gte", "lte"],
            "sysop": ["iexact", "icontains"],
            # DimRf
            "info_rf__tx_mhz": ["exact", "gte", "lte"],
            "info_rf__rx_mhz": ["exact", "gte", "lte"],
            "info_rf__channel": ["iexact"],
            "info_rf__band": ["iexact"],
            "info_rf__mode": ["iexact"],
            "info_rf__shift_mhz": ["exact", "gte", "lte"],
            # DimFm
            "info_fm__modulation": ["iexact", "icontains"],
            "info_fm__tone": ["exact"],
            "info_fm__bandwidth": ["iexact"],
            # DimDStar
            "info_dstar__modulation": ["iexact", "icontains"],
            "info_dstar__gateway": ["iexact"],
            "info_dstar__reflector": ["iexact"],
            # DimFusion
            "info_fusion__modulation": ["iexact", "icontains"],
            "info_fusion__wiresx": ["iexact"],
            "info_fusion__room_id": ["iexact"],
            # DimDmr
            "info_dmr__modulation": ["iexact", "icontains"],
            "info_dmr__tg__name": ["iexact", "icontains"],
            "info_dmr__tg__id": ["exact"],
            "info_dmr__ts1_default_tg__name": ["iexact", "icontains"],
            "info_dmr__ts1_default_tg__id": ["exact"],
            "info_dmr__ts2_default_tg__name": ["iexact", "icontains"],
            "info_dmr__ts2_default_tg__id": ["exact"],
            # DimHolder
            "info_holder__abrv": ["iexact", "icontains"],
            "info_holder__name": ["iexact", "icontains"],
            # DimLocation
            "info_location__latitude": ["exact", "gte", "lte"],
            "info_location__longitude": ["exact", "gte", "lte"],
            "info_location__region": ["iexact"],
            "info_location__place": ["iexact", "icontains"],
            "info_location__qth_loc": ["iexact"],
        }

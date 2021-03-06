import re
from functools import reduce

from django.db.models import Q

automatic_fields = {
    # FactRepeater
    "callsign": ["exact", "iexact", "icontains"],
    "notes": ["exact", "icontains"],
    "pwr_w": ["exact", "gte", "lte"],
    "info_half_duplex": ["isnull"],
    "info_simplex": ["isnull"],
    "info_fm": ["isnull"],
    "info_dstar": ["isnull"],
    "info_fusion": ["isnull"],
    "info_dmr": ["isnull"],
    "info_holder": ["isnull"],
    "info_location": ["isnull"],
    "sysop": ["exact", "iexact", "icontains"],
    # DimHalfDuplex
    "info_half_duplex__tx_mhz": ["exact", "gte", "lte"],
    "info_half_duplex__rx_mhz": ["exact", "gte", "lte"],
    "info_half_duplex__channel": ["exact", "iexact"],
    # DimSimplex
    "info_simplex__freq_mhz": ["exact", "gte", "lte"],
    "info_simplex__channel": ["exact", "iexact"],
    # DimFm
    "info_fm__modulation": ["exact", "iexact", "icontains"],
    "info_fm__tone": ["exact", "gte", "lte"],
    # DimDStar
    "info_dstar__modulation": ["exact", "iexact", "icontains"],
    "info_dstar__gateway": ["exact", "iexact", "icontains"],
    "info_dstar__reflector": ["exact", "iexact", "icontains"],
    # DimFusion
    "info_fusion__modulation": ["exact", "iexact", "icontains"],
    "info_fusion__wiresx": ["exact", "iexact", "icontains"],
    "info_fusion__room_id": ["exact", "iexact", "icontains"],
    # DimDmr
    "info_dmr__modulation": ["exact", "iexact", "icontains"],
    "info_dmr__dmr_id": ["exact", "gte", "lte"],
    "info_dmr__color_code": ["exact", "gte", "lte"],
    "info_dmr__ts1_default_tg__name": ["exact", "iexact", "icontains"],
    "info_dmr__ts1_default_tg__dmr_id": ["exact", "gte", "lte"],
    "info_dmr__ts2_default_tg__name": ["exact", "iexact", "icontains"],
    "info_dmr__ts2_default_tg__dmr_id": ["exact", "gte", "lte"],
    # DimHolder
    "info_holder__abrv": ["exact", "iexact", "icontains"],
    "info_holder__name": ["exact", "iexact", "icontains"],
    # DimLocation
    "info_location__latitude": ["exact", "gte", "lte"],
    "info_location__longitude": ["exact", "gte", "lte"],
    "info_location__region": ["exact"],
    "info_location__place": ["exact", "icontains"],
    "info_location__qth_loc": ["exact", "iexact"],
}


def modulation_search(queryset, name, value):
    queryset = queryset.filter(
        Q(info_fm__modulation__icontains=value)
        | Q(info_dstar__modulation__icontains=value)
        | Q(info_fusion__modulation__icontains=value)
        | Q(info_dmr__modulation__icontains=value)
    )
    return queryset


def holder_search(queryset, name, value):
    queryset = queryset.filter(
        Q(info_holder__abrv__icontains=value) | Q(info_holder__name__icontains=value)
    )
    return queryset


def mode_search(queryset, name, value):
    modes = re.findall(r"[\w]+", value)
    queryset_filter = None
    if "fm" in modes:
        new_filter = Q(info_fm__isnull=False)
        if queryset_filter is None:
            queryset_filter = new_filter
        else:
            queryset_filter |= new_filter
    if "dstar" in modes:
        new_filter = Q(info_dstar__isnull=False)
        if queryset_filter is None:
            queryset_filter = new_filter
        else:
            queryset_filter |= new_filter
    if "fusion" in modes:
        new_filter = Q(info_fusion__isnull=False)
        if queryset_filter is None:
            queryset_filter = new_filter
        else:
            queryset_filter |= new_filter
    if "dmr" in modes:
        new_filter = Q(info_dmr__isnull=False)
        if queryset_filter is None:
            queryset_filter = new_filter
        else:
            queryset_filter |= new_filter
    return queryset.filter(queryset_filter)


def rf_search(queryset, name, value):
    modes = re.findall(r"[\w]+", value)
    queryset_filter = None
    if "half_duplex" in modes:
        if queryset_filter is None:
            queryset_filter = Q(info_half_duplex__isnull=False)
        else:
            queryset_filter |= Q(info_half_duplex__isnull=False)
    if "simplex" in modes:
        if queryset_filter is None:
            queryset_filter = Q(info_simplex__isnull=False)
        else:
            queryset_filter |= Q(info_simplex__isnull=False)
    return queryset.filter(queryset_filter)


def freq_mhz_search(queryset, name, value):
    queryset = queryset.filter(
        Q(info_half_duplex__tx_mhz__exact=value)
        | Q(info_half_duplex__rx_mhz__exact=value)
        | Q(info_simplex__freq_mhz__exact=value)
    )
    return queryset


def freq_mhz_search__gte(queryset, name, value):
    queryset = queryset.filter(
        Q(info_half_duplex__tx_mhz__gte=value)
        | Q(info_half_duplex__rx_mhz__gte=value)
        | Q(info_simplex__freq_mhz__gte=value)
    )
    return queryset


def freq_mhz_search__lte(queryset, name, value):
    queryset = queryset.filter(
        Q(info_half_duplex__tx_mhz__lte=value)
        | Q(info_half_duplex__rx_mhz__lte=value)
        | Q(info_simplex__freq_mhz__lte=value)
    )
    return queryset


def region_search(queryset, name, value):
    regions = re.findall(r"[\w]+", value)
    queryset_filtered = queryset.filter(
        reduce(lambda x, y: x | y, [Q(info_location__region=r) for r in regions])
    )
    return queryset_filtered

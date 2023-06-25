import re
from functools import reduce

from django.db.models import Q

from repeaters.models import FactRepeater

automatic_fields = {
    # FactRepeater
    "callsign": ["iexact", "icontains"],
    "notes": ["icontains"],
    "pwr_w": ["exact", "gte", "lte"],
    "info_half_duplex": ["isnull"],
    "info_simplex": ["isnull"],
    "info_fm": ["isnull"],
    "info_dstar": ["isnull"],
    "info_fusion": ["isnull"],
    "info_dmr": ["isnull"],
    "info_holder": ["isnull"],
    "info_location": ["isnull"],
    "sysop": ["iexact", "icontains"],
    # DimHalfDuplex
    "info_half_duplex__tx_mhz": ["exact", "gte", "lte"],
    "info_half_duplex__rx_mhz": ["exact", "gte", "lte"],
    "info_half_duplex__channel": ["iexact"],
    # DimSimplex
    "info_simplex__freq_mhz": ["exact", "gte", "lte"],
    "info_simplex__channel": ["iexact"],
    # DimFm
    "info_fm__modulation": ["iexact", "icontains"],
    "info_fm__tone": ["exact", "gte", "lte"],
    # DimDStar
    "info_dstar__modulation": ["iexact", "icontains"],
    "info_dstar__gateway": ["iexact", "icontains"],
    "info_dstar__reflector": ["iexact", "icontains"],
    # DimFusion
    "info_fusion__modulation": ["iexact", "icontains"],
    "info_fusion__wiresx": ["iexact", "icontains"],
    "info_fusion__room_id": ["iexact", "icontains"],
    # DimDmr
    "info_dmr__modulation": ["iexact", "icontains"],
    "info_dmr__id": ["exact", "gte", "lte"],
    "info_dmr__color_code": ["exact", "gte", "lte"],
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
    "info_location__region": ["exact"],
    "info_location__place": ["exact", "icontains"],
    "info_location__qth_loc": ["iexact", "icontains"],
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


def modes_search(queryset, name, value):
    modes = re.findall(r"[\w]+", value)
    allowed_modes = {
        FactRepeater.ModeOptions.FM,
        FactRepeater.ModeOptions.DSTAR,
        FactRepeater.ModeOptions.FUSION,
        FactRepeater.ModeOptions.DMR,
    }
    query_modes = list({mode.lower() for mode in modes} & allowed_modes)
    return queryset.filter(modes__overlap=query_modes)


def rf_search(queryset, name, value):
    modes = re.findall(r"(?:\b\w+-\w+\b|\b\w+\b)", value)
    queryset_filter = Q()
    modes_to_consider = {mode.lower() for mode in modes} & {
        FactRepeater.RfOptions.HALF_DUPLEX,
        FactRepeater.RfOptions.SIMPLEX,
    }
    for mode in modes_to_consider:
        queryset_filter |= Q(rf=mode)
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


def band_seach(queryset, name, value):
    band = re.findall(r"[\w]+", value)
    queryset_filtered = queryset.filter(
        reduce(lambda x, y: x | y, [Q(band__icontains=b) for b in band])
    )
    return queryset_filtered

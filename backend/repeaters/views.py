from django.db.models import Q
from rest_framework import viewsets
from django_filters import rest_framework as filters
from .models import FactRepeater
from .serializers import FactRepeaterSerializer


class FactRepeaterFilter(filters.FilterSet):
    # https://stackoverflow.com/a/62878113/5168563
    modulation = filters.CharFilter(label="modulation", method="modulation_search")
    holder = filters.CharFilter(label="holder", method="holder_search")

    mode = filters.CharFilter(label="mode", method="mode_search")
    rf = filters.CharFilter(label="rf", method="rf_search")

    freq_mhz = filters.NumberFilter(label="freq_mhz", method="freq_mhz_search")
    freq_mhz__gte = filters.NumberFilter(
        label="freq_mhz__gte", method="freq_mhz_search__gte"
    )
    freq_mhz__lte = filters.NumberFilter(
        label="freq_mhz__lte", method="freq_mhz_search__lte"
    )

    def modulation_search(self, queryset, name, value):
        queryset = queryset.filter(
            Q(info_fm__modulation__icontains=value)
            | Q(info_dstar__modulation__icontains=value)
            | Q(info_fusion__modulation__icontains=value)
            | Q(info_dmr__modulation__icontains=value)
        )
        return queryset

    def holder_search(self, queryset, name, value):
        queryset = queryset.filter(
            Q(info_holder__abrv__icontains=value)
            | Q(info_holder__name__icontains=value)
        )
        return queryset

    def mode_search(self, queryset, name, value):
        modes = value.split(",").split(" ")
        filter = None
        if "fm" in modes:
            if filter is None:
                filter = Q(info_fm__isnull=False)
            else:
                filter = filter | Q(info_fm__isnull=False)
        if "dstar" in modes:
            if filter is None:
                filter = Q(info_dstar__isnull=False)
            else:
                filter = filter | Q(info_dstar__isnull=False)
        if "fusion" in modes:
            if filter is None:
                filter = Q(info_fusion__isnull=False)
            else:
                filter = filter | Q(info_fusion__isnull=False)
        if "dmr" in modes:
            if filter is None:
                filter = Q(info_dmr__isnull=False)
            else:
                filter = filter | Q(info_dmr__isnull=False)
        return queryset.filter(filter)

    def rf_search(self, queryset, name, value):
        modes = value.split(",").split(" ")
        filter = None
        if "half_duplex" in modes:
            if filter is None:
                filter = Q(info_half_duplex__isnull=False)
            else:
                filter = filter | Q(info_half_duplex__isnull=False)
        if "simplex" in modes:
            if filter is None:
                filter = Q(info_simplex__isnull=False)
            else:
                filter = filter | Q(info_simplex__isnull=False)
        return queryset.filter(filter)

    def freq_mhz_search(self, queryset, name, value):
        queryset = queryset.filter(
            Q(info_half_duplex__tx_mhz__exact=value)
            | Q(info_half_duplex__rx_mhz__exact=value)
            | Q(info_simplex__freq_mhz__exact=value)
        )
        return queryset

    def freq_mhz_search__gte(self, queryset, name, value):
        queryset = queryset.filter(
            Q(info_half_duplex__tx_mhz__gte=value)
            | Q(info_half_duplex__rx_mhz__gte=value)
            | Q(info_simplex__freq_mhz__gte=value)
        )
        return queryset

    def freq_mhz_search__lte(self, queryset, name, value):
        queryset = queryset.filter(
            Q(info_half_duplex__tx_mhz__lte=value)
            | Q(info_half_duplex__rx_mhz__lte=value)
            | Q(info_simplex__freq_mhz__lte=value)
        )
        return queryset

    class Meta:
        model = FactRepeater
        fields = {
            # FactRepeater
            "callsign": ["exact", "iexact", "icontains"],
            "notes": ["exact", "icontains"],
            "sysop": ["exact", "iexact", "icontains"],
            "pwr_w": ["exact", "gte", "lte"],
            "info_half_duplex": ["isnull"],
            "info_simplex": ["isnull"],
            "info_fm": ["isnull"],
            "info_dstar": ["isnull"],
            "info_fusion": ["isnull"],
            "info_dmr": ["isnull"],
            "info_holder": ["isnull"],
            "info_location": ["isnull"],
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
            "info_dmr__ts1_configuration": ["exact", "icontains"],
            "info_dmr__ts2_configuration": ["exact", "icontains"],
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


class FactRepeaterViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows FactRepeaters (repeater objects) to be viewed or edited.

    Example of return value:
    (for more details, read the source code in `./backend/repeaters/models.py`)
    ```js
    [
        {
            "id": 1,
            "info_half_duplex": {
                "id": 1,
                "shift": 0.6,
                "tx_mhz": "144.8000000000", // string-like because it uses Decimal types
                "rx_mhz": "144.2000000000",
                "channel": null
            },
            "info_simplex": null,
            "info_fm": {
                "id": 1,
                "modulation": "11kHzF3E",
                "tone": "123.0000000000"
            },
            "info_dstar": null,
            "info_fusion": null,
            "info_dmr": null,
            "info_holder": {
                "id": 1,
                "abrv": "ARBA",
                "name": ""
            },
            "info_location": {
                "id": 1,
                "latitude": null,
                "longitude": null,
                "region": "CPT", // CPT, AZR, MDA, OT
                "place": "Serra do Marao",
                "qth_loc": ""
            },
            "callsign": "CQ0VMA",
            "notes": "",
            "sysop": "",
            "pwr_w": 50
        },
        // ...
    ]

    ```

    The API includes rich filtering facilities.

    This is the full possible query, but not all fiels are useful.
    The query follows the same syntax as Django's filter system:
        https://docs.djangoproject.com/en/3.2/ref/models/querysets/#field-lookups
    Check below for the recomended fields.

    ```
    `GET /api/v1/repeaters/?
        callsign=
        &callsign__iexact=
        &callsign__icontains=
        &notes=
        &notes__icontains=
        &sysop=
        &sysop__iexact=
        &sysop__icontains=
        &pwr_w=
        &pwr_w__gte=
        &pwr_w__lte=
        &info_half_duplex__isnull=
        &info_simplex__isnull=
        &info_fm__isnull=
        &info_dstar__isnull=
        &info_fusion__isnull=
        &info_dmr__isnull=
        &info_holder__isnull=
        &info_location__isnull=
        &info_half_duplex__tx_mhz=
        &info_half_duplex__tx_mhz__gte=
        &info_half_duplex__tx_mhz__lte=
        &info_half_duplex__rx_mhz=
        &info_half_duplex__rx_mhz__gte=
        &info_half_duplex__rx_mhz__lte=
        &info_half_duplex__channel=
        &info_half_duplex__channel__iexact=
        &info_simplex__freq_mhz=
        &info_simplex__freq_mhz__gte=
        &info_simplex__freq_mhz__lte=
        &info_simplex__channel=
        &info_simplex__channel__iexact=
        &info_fm__modulation=
        &info_fm__modulation__iexact=
        &info_fm__modulation__icontains=
        &info_fm__tone=
        &info_fm__tone__gte=
        &info_fm__tone__lte=
        &info_dstar__modulation=
        &info_dstar__modulation__iexact=
        &info_dstar__modulation__icontains=
        &info_dstar__gateway=
        &info_dstar__gateway__iexact=
        &info_dstar__gateway__icontains=
        &info_dstar__reflector=
        &info_dstar__reflector__iexact=
        &info_dstar__reflector__icontains=
        &info_fusion__modulation=
        &info_fusion__modulation__iexact=
        &info_fusion__modulation__icontains=
        &info_fusion__wiresx=
        &info_fusion__wiresx__iexact=
        &info_fusion__wiresx__icontains=
        &info_fusion__room_id=
        &info_fusion__room_id__iexact=
        &info_fusion__room_id__icontains=
        &info_dmr__modulation=
        &info_dmr__modulation__iexact=
        &info_dmr__modulation__icontains=
        &info_dmr__dmr_id=
        &info_dmr__dmr_id__gte=
        &info_dmr__dmr_id__lte=
        &info_dmr__color_code=
        &info_dmr__color_code__gte=
        &info_dmr__color_code__lte=
        &info_dmr__ts1_configuration=
        &info_dmr__ts1_configuration__icontains=
        &info_dmr__ts2_configuration=
        &info_dmr__ts2_configuration__icontains=
        &info_holder__abrv=
        &info_holder__abrv__iexact=
        &info_holder__abrv__icontains=
        &info_holder__name=
        &info_holder__name__iexact=
        &info_holder__name__icontains=
        &info_location__latitude=
        &info_location__latitude__gte=
        &info_location__latitude__lte=
        &info_location__longitude=
        &info_location__longitude__gte=
        &info_location__longitude__lte=
        &info_location__region=
        &info_location__place=
        &info_location__place__icontains=
        &info_location__qth_loc=
        &info_location__qth_loc__iexact=
        &modulation=
        &holder=
        &mode=
        &rf=
        &freq_mhz=
        &freq_mhz__gte=
        &freq_mhz__lte=
    ```

    As stated, a smaller set of these fields make for a better, and complete query.
    The recomended fields are:

    ```
    GET /api/v1/repeaters/?
        callsign__icontains= // Callsign partial match, case insensitive
        &notes__icontains= // Notes partial match, case insensitive
        &sysop__icontains= // Sysop partial match, case insensitive
        &pwr_w= // Power in watts, exact match
        &pwr_w__gte= // Power in watts, greater than or equal to
        &pwr_w__lte= // Power in watts, less than or equal to
        &info_fm__tone= // FM tone, exact match
        &info_fm__tone__gte= // FM tone, greater than or equal to
        &info_fm__tone__lte= // FM tone, less than or equal to
        &info_dstar__gateway__icontains= // D-STAR gateway, partial match, case insensitive
        &info_dstar__reflector__icontains= // D-STAR reflector, partial match, case insensitive
        &info_fusion__wiresx__icontains= // Fusion WIRES-X, partial match, case insensitive
        &info_fusion__room_id__icontains= // Fusion Room ID, partial match, case insensitive
        &info_dmr__dmr_id= // DMR ID, exact match
        &info_dmr__dmr_id__gte= // DMR ID, greater than or equal to
        &info_dmr__dmr_id__lte= // DMR ID, less than or equal to
        &info_dmr__color_code= // DMR color code, exact match
        &info_dmr__color_code__gte= // DMR color code, greater than or equal to
        &info_dmr__color_code__lte= // DMR color code, less than or equal to
        &info_dmr__ts1_configuration__icontains= // DMR TS1 configuration, partial match, case insensitive
        &info_dmr__ts2_configuration__icontains= // DMR TS2 configuration, partial match, case insensitive
        &info_location__latitude= // Latitude, exact match
        &info_location__latitude__gte= // Latitude, greater than or equal to
        &info_location__latitude__lte= // Latitude, less than or equal to
        &info_location__longitude= // Longitude, exact match
        &info_location__longitude__gte= // Longitude, greater than or equal to
        &info_location__longitude__lte= // Longitude, less than or equal to
        &info_location__region= // Region, exact match
            // The possible values are: ["CPT", "AZR", "MDA", "OT"] (no quotes)
            // Meaning "Portugal continental", "Açores", "Madeira", "Other", respectively
        &info_location__place__icontains= // Place, partial match, case insensitive
        &info_location__qth_loc__iexact= // QTH locator, exact match, case insensitive
        &modulation= // Modulation, partial match, case insensitive, across *all* modulation fields
        &holder= // Holder, partial match, case insensitive, across *all* holder fields
        &mode= // Filtering for repeater mode. Multiple values are allowed, comma separated
            // Multiple values are ORed together
            // Possible values are: ["fm","dstar","fusion","dmr"] (no quotes)
            // Ex.: to filter for repeaters that are either FM or DMR repeaters, use:
            // `&mode=fm,dmr`
        &rf= // Filtering for "RF mode" (simplex/half-duplex). Multiple values are allowed, comma separated
            // Works as the `&mode case`
            // Possible values are: ["simplex","half_duplex"] (no quotes)
        &freq_mhz= // Filters for frequency across all frequency fields, both simplex,
            // and half-duplex, both Tx and Rx.
        &freq_mhz__gte= // As above, but greater than or equal to
        &freq_mhz__lte= // As above, but less than or equal to
    ```


    """

    queryset = FactRepeater.objects.all()
    serializer_class = FactRepeaterSerializer

    filterset_class = FactRepeaterFilter

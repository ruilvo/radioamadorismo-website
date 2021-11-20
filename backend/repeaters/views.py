from rest_framework import viewsets
from django_filters import rest_framework as filters
from .models import FactRepeater
from .serializers import FactRepeaterSerializer


class FactRepeaterFilter(filters.FilterSet):
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
    queryset = FactRepeater.objects.all()
    serializer_class = FactRepeaterSerializer

    filterset_class = FactRepeaterFilter

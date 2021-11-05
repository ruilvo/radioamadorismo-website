from rest_framework import serializers

from .models import (
    DimHalfDuplex,
    DimSimplex,
    DimFm,
    DimDStar,
    DimFusion,
    DimDmr,
    DimHolder,
    DimLocation,
    FactRepeater,
)


class DimHalfDuplexSerializer(serializers.ModelSerializer):
    shift = serializers.ReadOnlyField()

    class Meta:
        model = DimHalfDuplex
        fields = "__all__"


class DimSimplexSerializer(serializers.ModelSerializer):
    class Meta:
        model = DimSimplex
        fields = "__all__"


class DimFmSerializer(serializers.ModelSerializer):
    class Meta:
        model = DimFm
        fields = "__all__"


class DimDStarSerializer(serializers.ModelSerializer):
    class Meta:
        model = DimDStar
        fields = "__all__"


class DimFusionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DimFusion
        fields = "__all__"


class DimDmrSerializer(serializers.ModelSerializer):
    class Meta:
        model = DimDmr
        fields = "__all__"


class DimHolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = DimHolder
        fields = "__all__"


class DimLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DimLocation
        fields = "__all__"


def get_update_DimHalfDuplex(info_half_duplex_data: dict) -> DimHalfDuplex or None:
    if info_half_duplex_data is not None:
        (
            info_half_duplex,
            info_half_duplex_created,
        ) = DimHalfDuplex.objects.get_or_create(
            tx_mhz=info_half_duplex_data["tx_mhz"],
            rx_mhz=info_half_duplex_data["rx_mhz"],
            defaults=info_half_duplex_data,
        )
        if (
            not info_half_duplex_created
            and info_half_duplex_data["channel"] is not None
        ):
            info_half_duplex.channel = info_half_duplex_data["channel"]
            info_half_duplex.save()
        return info_half_duplex
    return None


def get_update_DimSimplex(info_simplex_data: dict) -> DimSimplex or None:
    if info_simplex_data is not None:
        info_simplex, info_simplex_created = DimSimplex.objects.get_or_create(
            freq_mhz=info_simplex_data["freq_mhz"], defaults=info_simplex_data
        )
        if not info_simplex_created and info_simplex_data["channel"] is not None:
            info_simplex.channel = info_simplex_data["channel"]
            info_simplex.save()
        return info_simplex
    return None


def get_update_DimFm(info_fm_data: dict) -> DimFm or None:
    if info_fm_data is not None:
        info_fm, _ = DimFm.objects.get_or_create(
            modulation=info_fm_data["modulation"],
            tone=info_fm_data["tone"],
            defaults=info_fm_data,
        )
        return info_fm
    return None


def get_update_DimDStar(info_dstar_data: dict) -> DimDStar or None:
    if info_dstar_data is not None:
        info_dstar, _ = DimDStar.objects.get_or_create(
            modulation=info_dstar_data["modulation"],
            gateway=info_dstar_data["gateway"],
            reflector=info_dstar_data["reflector"],
            defaults=info_dstar_data,
        )
        return info_dstar
    return None


def get_update_DimFusion(info_fusion_data: dict) -> DimFusion or None:
    if info_fusion_data is not None:
        info_fusion, _ = DimDStar.objects.get_or_create(
            wiresx=info_fusion_data["wiresx"],
            room_id=info_fusion_data["room_id"],
            defaults=info_fusion_data,
        )
        return info_fusion
    return None


def get_update_DimDmr(info_dmr_data: dict) -> DimDmr or None:
    if info_dmr_data is not None:
        info_dmr, info_dmr_created = DimDmr.objects.get_or_create(
            dmr_id=info_dmr_data["dmr_id"],
            defaults=info_dmr_data,
        )
        if not info_dmr_created:
            # Check for the optional fields that are to be updated
            if info_dmr_data["modulation"] is not None:
                info_dmr.modulation = info_dmr_data["modulation"]
            if info_dmr_data["color_code"] is not None:
                info_dmr.color_code = info_dmr_data["color_code"]
            if info_dmr_data["ts1_configuration"] is not None:
                info_dmr.ts1_configuration = info_dmr_data["ts1_configuration"]
            if info_dmr_data["ts2_configuration"] is not None:
                info_dmr.ts2_configuration = info_dmr_data["ts2_configuration"]
            info_dmr.save()
        return info_dmr
    return None


def get_update_DimHolder(info_holder_data: dict) -> DimHolder or None:
    if info_holder_data is not None:
        info_holder, info_holder_created = DimHolder.objects.get_or_create(
            abrv=info_holder_data["abrv"],
            defaults=info_holder_data,
        )
        if not info_holder_created and info_holder_data["name"] is not None:
            info_holder.name = info_holder_data["name"]
            info_holder.save()
        return info_holder
    return None


def get_update_DimLocation(info_location_data: dict) -> DimLocation or None:
    if info_location_data is not None:
        (info_location, info_location_created,) = DimLocation.objects.get_or_create(
            latitude=info_location_data["latitude"],
            longitude=info_location_data["longitude"],
            defaults=info_location_data,
        )
        if not info_location_created:
            # Check for the optional fields that are to be updated
            if info_location_data["region"] is not None:
                info_location.region = info_location_data["region"]
            if info_location_data["place"] is not None:
                info_location.place = info_location_data["place"]
            if info_location_data["qth_loc"] is not None:
                info_location.qth_loc = info_location_data["qth_loc"]
            info_location.save()
        return info_location
    return None


class FactRepeaterSerializer(serializers.ModelSerializer):
    info_half_duplex = DimHalfDuplexSerializer(many=False, required=False)
    info_simplex = DimSimplexSerializer(many=False, required=False)
    info_fm = DimFmSerializer(many=False, required=False)
    info_dstar = DimDStarSerializer(many=False, required=False)
    info_fusion = DimFusionSerializer(many=False, required=False)
    info_dmr = DimDmrSerializer(many=False, required=False)
    info_holder = DimHolderSerializer(many=False, required=False)
    info_location = DimLocationSerializer(many=False, required=False)

    class Meta:
        model = FactRepeater
        fields = "__all__"

    # https://www.django-rest-framework.org/api-guide/relations/#writable-nested-serializers
    # I should write a test for this one...
    def create(self, validated_data):

        info_half_duplex = get_update_DimHalfDuplex(
            validated_data.pop("info_half_duplex", None)
        )
        info_simplex = get_update_DimSimplex(validated_data.pop("info_simplex", None))
        info_fm = get_update_DimFm(validated_data.pop("info_fm", None))
        info_dstar = get_update_DimDStar(validated_data.pop("info_dstar", None))
        info_fusion = get_update_DimFusion(validated_data.pop("info_fusion", None))
        info_dmr = get_update_DimDmr(validated_data.pop("info_dmr", None))
        info_holder = get_update_DimHolder(validated_data.pop("info_holder", None))
        info_location = get_update_DimLocation(
            validated_data.pop("info_location", None)
        )

        repeater = FactRepeater.objects.create(
            info_half_duplex=info_half_duplex,
            info_simplex=info_simplex,
            info_fm=info_fm,
            info_fusion=info_fusion,
            info_dstar=info_dstar,
            info_dmr=info_dmr,
            info_holder=info_holder,
            info_location=info_location,
            **validated_data
        )

        return repeater

    def update(self, instance, validated_data):

        info_half_duplex = get_update_DimHalfDuplex(
            validated_data.pop("info_half_duplex", None)
        )
        instance.info_half_duplex = (
            info_half_duplex
            if info_half_duplex is not None
            else instance.info_half_duplex
        )

        info_simplex = get_update_DimSimplex(validated_data.pop("info_simplex", None))
        instance.info_simplex = (
            info_simplex if info_simplex is not None else instance.info_simplex
        )

        info_fm = get_update_DimFm(validated_data.pop("info_fm", None))
        instance.info_fm = info_fm if info_fm is not None else instance.info_fm

        info_dstar = get_update_DimDStar(validated_data.pop("info_dstar", None))
        instance.info_dstar = (
            info_dstar if info_dstar is not None else instance.info_dstar
        )

        info_fusion = get_update_DimFusion(validated_data.pop("info_fusion", None))
        instance.info_fusion = (
            info_fusion if info_fusion is not None else instance.info_fusion
        )

        info_dmr = get_update_DimDmr(validated_data.pop("info_dmr", None))
        instance.info_dmr = info_dmr if info_dmr is not None else instance.info_dmr

        info_holder = get_update_DimHolder(validated_data.pop("info_holder", None))
        instance.info_holder = (
            info_holder if info_holder is not None else instance.info_holder
        )

        info_location = get_update_DimLocation(
            validated_data.pop("info_location", None)
        )
        instance.info_location = (
            info_location if info_location is not None else instance.info_location
        )

        instance.callsign = validated_data.get("callsign", instance.callsign)
        instance.notes = validated_data.get("notes", instance.notes)
        instance.sysop = validated_data.get("sysop", instance.sysop)
        instance.pwr_w = validated_data.get("pwr_w", instance.pwr_w)

        instance.save()

        return instance

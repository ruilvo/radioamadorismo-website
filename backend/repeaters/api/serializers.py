"""
Serializers for the repeaters API.
"""

from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers

from drf_writable_nested.serializers import WritableNestedModelSerializer
from drf_writable_nested.mixins import UniqueFieldsMixin

from repeaters.models import (
    DimRf,
    DimFm,
    DimDStar,
    DimFusion,
    DimDmrTg,
    DimDmr,
    DimHolder,
    DimLocation,
    FactRepeater,
)


class DimRfSerializer(UniqueFieldsMixin, serializers.ModelSerializer):
    __doc__ = DimRf.__doc__

    class Meta:
        model = DimRf
        fields = "__all__"

    def create(self, validated_data):
        tx_mhz = validated_data["tx_mhz"]
        rx_mhz = validated_data["rx_mhz"]
        new_object, new_object_created = DimRf.objects.get_or_create(
            tx_mhz=tx_mhz, rx_mhz=rx_mhz, defaults=validated_data
        )
        if new_object_created:
            return new_object
        channel = validated_data.get("channel", None)
        if channel is not None:
            new_object.channel = channel
            new_object.save()
        return new_object


class DimFmSerializer(UniqueFieldsMixin, serializers.ModelSerializer):
    __doc__ = DimFm.__doc__

    class Meta:
        model = DimFm
        fields = "__all__"

    def create(self, validated_data):
        modulation = validated_data["modulation"]
        tone = validated_data.get("tone", None)
        if modulation is not None and tone is not None:
            new_object, _ = DimFm.objects.get_or_create(
                modulation=modulation, tone=tone, defaults=validated_data
            )
            return new_object
        return DimFm.objects.create(**validated_data)


class DimDStarSerializer(UniqueFieldsMixin, serializers.ModelSerializer):
    __doc__ = DimDStar.__doc__

    class Meta:
        model = DimDStar
        fields = "__all__"

    def create(self, validated_data):
        modulation = validated_data.get("modulation", None)
        gateway = validated_data.get("gateway", None)
        reflector = validated_data.get("reflector", None)
        if gateway is not None and reflector is not None:
            new_object, new_object_created = DimDStar.objects.get_or_create(
                gateway=gateway,
                reflector=reflector,
                defaults=validated_data,
            )
            if not new_object_created and modulation is not None:
                new_object.modulation = modulation
                new_object.save()
            return new_object
        return DimDStar.objects.create(**validated_data)


class DimFusionSerializer(UniqueFieldsMixin, serializers.ModelSerializer):
    __doc__ = DimFusion.__doc__

    class Meta:
        model = DimFusion
        fields = "__all__"

    def create(self, validated_data):
        modulation = validated_data.get("modulation", None)
        wiresx = validated_data.get("wiresx", None)
        room_id = validated_data.get("room_id", None)
        if wiresx is not None and room_id is not None:
            new_object, new_object_created = DimFusion.objects.get_or_create(
                wiresx=wiresx,
                room_id=room_id,
                defaults=validated_data,
            )
            if not new_object_created and modulation is not None:
                new_object.modulation = modulation
                new_object.save()
            return new_object
        return DimFusion.objects.create(**validated_data)


class DimDmrTgSerializer(UniqueFieldsMixin, serializers.ModelSerializer):
    __doc__ = DimDmrTg.__doc__

    class Meta:
        model = DimDmrTg
        fields = "__all__"

    def create(self, validated_data):
        name = validated_data.get("name", None)
        id = validated_data.get(  # pylint: disable=invalid-name,redefined-builtin
            "id", None
        )
        call_mode = validated_data.get("call_mode", None)
        if id is not None:
            new_object, new_object_created = DimDmrTg.objects.get_or_create(
                id=id,
                defaults=validated_data,
            )
            if not new_object_created:
                new_object.name = name
                new_object.call_mode = call_mode
                new_object.save()
            return new_object
        return DimDmrTg.objects.create(**validated_data)


class DimDmrSerializer(  # pylint: disable=too-many-ancestors
    UniqueFieldsMixin, WritableNestedModelSerializer
):
    __doc__ = DimDmr.__doc__

    tg = DimDmrTgSerializer(many=False, required=True)
    ts1_default_tg = DimDmrTgSerializer(many=False, required=False)
    ts2_default_tg = DimDmrTgSerializer(many=False, required=False)
    ts1_alternative_tgs = DimDmrTgSerializer(many=True, required=False)
    ts2_alternative_tgs = DimDmrTgSerializer(many=True, required=False)

    class Meta:
        model = DimDmr
        fields = "__all__"

    def create(self, validated_data):
        try:
            return DimDmr.objects.get(tg__id=validated_data["tg"]["id"])
            # TODO(ruilvo, 2023-08-05): This is a hack to avoid creating duplicate
            # objects. This needs some fixing, in particular updating
            # the other fields in case they have changed.
        except ObjectDoesNotExist:
            return super().create(validated_data)


class DimHolderSerializer(UniqueFieldsMixin, serializers.ModelSerializer):
    __doc__ = DimHolder.__doc__

    class Meta:
        model = DimHolder
        fields = "__all__"

    def create(self, validated_data):
        abrv = validated_data.get("abrv", None)
        name = validated_data.get("name", None)
        if abrv is not None:
            new_object, new_object_created = DimHolder.objects.get_or_create(
                abrv=abrv,
                defaults=validated_data,
            )
            if not new_object_created:
                if name is not None:
                    new_object.name = name
                new_object.save()
            return new_object
        return DimHolder.objects.create(**validated_data)


class DimLocationSerializer(UniqueFieldsMixin, serializers.ModelSerializer):
    __doc__ = DimLocation.__doc__

    class Meta:
        model = DimLocation
        fields = "__all__"

    def create(self, validated_data):
        latitude = validated_data.get("latitude", None)
        longitude = validated_data.get("longitude", None)
        region = validated_data.get("region", None)
        place = validated_data.get("place", None)
        qth_loc = validated_data.get("qth_loc", None)
        if latitude is not None and longitude is not None:
            new_object, new_object_created = DimLocation.objects.get_or_create(
                latitude=latitude,
                longitude=longitude,
                defaults=validated_data,
            )
            if not new_object_created:
                if region is not None:
                    new_object.region = region
                if place is not None:
                    new_object.place = place
                if qth_loc is not None:
                    new_object.qth_loc = qth_loc
                new_object.save()
            return new_object
        return DimLocation.objects.create(**validated_data)


class FactRepeaterSerializer(  # pylint: disable=too-many-ancestors
    WritableNestedModelSerializer
):
    __doc__ = FactRepeater.__doc__

    info_rf = DimRfSerializer(many=False, required=False)
    info_fm = DimFmSerializer(many=False, required=False)
    info_dstar = DimDStarSerializer(many=False, required=False)
    info_fusion = DimFusionSerializer(many=False, required=False)
    info_dmr = DimDmrSerializer(many=False, required=False)
    info_holder = DimHolderSerializer(many=False, required=False)
    info_location = DimLocationSerializer(many=False, required=False)

    class Meta:
        model = FactRepeater
        fields = "__all__"

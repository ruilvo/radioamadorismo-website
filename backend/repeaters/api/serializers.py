"""
Serializers for the repeaters API.
"""

from rest_framework import serializers

from drf_writable_nested.serializers import WritableNestedModelSerializer
from drf_writable_nested.mixins import UniqueFieldsMixin

from associations.api.serializers import AssociationSerializer

from repeaters.models import (
    DimRf,
    DimFm,
    DimDStar,
    DimFusion,
    DimDmrTg,
    DimDmr,
    DimTetra,
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
            new_object, new_object_created = DimFm.objects.get_or_create(
                modulation=modulation, tone=tone, defaults=validated_data
            )
            if not new_object_created:
                new_object.bandwidth = validated_data["bandwidth"]
                new_object.save()
            return new_object
        return DimFm.objects.create(**validated_data)


class DimDStarSerializer(UniqueFieldsMixin, serializers.ModelSerializer):
    __doc__ = DimDStar.__doc__

    class Meta:
        model = DimDStar
        fields = "__all__"

    def create(self, validated_data):
        gateway = validated_data["gateway"]
        reflector = validated_data["reflector"]
        new_object, new_object_created = DimDStar.objects.get_or_create(
            gateway=gateway,
            reflector=reflector,
            defaults=validated_data,
        )
        if not new_object_created:
            new_object.modulation = validated_data["modulation"]
            new_object.save()
        return new_object


class DimFusionSerializer(UniqueFieldsMixin, serializers.ModelSerializer):
    __doc__ = DimFusion.__doc__

    class Meta:
        model = DimFusion
        fields = "__all__"

    def create(self, validated_data):
        wiresx = validated_data["wiresx"]
        room_id = validated_data["room_id"]
        new_object, new_object_created = DimFusion.objects.get_or_create(
            wiresx=wiresx,
            room_id=room_id,
            defaults=validated_data,
        )
        if not new_object_created:
            new_object.modulation = validated_data["modulation"]
            new_object.save()
        return new_object


class DimDmrTgSerializer(UniqueFieldsMixin, serializers.ModelSerializer):
    __doc__ = DimDmrTg.__doc__

    class Meta:
        model = DimDmrTg
        fields = "__all__"

    def create(self, validated_data):
        id = validated_data["id"]  # pylint: disable=invalid-name,redefined-builtin
        new_object, new_object_created = DimDmrTg.objects.get_or_create(
            id=id,
            defaults=validated_data,
        )
        if not new_object_created:
            new_object.name = validated_data["name"]
            try:
                new_object.call_mode = validated_data["call_mode"]
            except KeyError:  # `call_mode` isn't always available, whatever.
                pass
            new_object.save()
        return new_object


class DimDmrSerializer(  # pylint: disable=too-many-ancestors
    UniqueFieldsMixin, WritableNestedModelSerializer
):
    __doc__ = DimDmr.__doc__

    tg = DimDmrTgSerializer(many=False, required=True)
    ts1_default_tg = DimDmrTgSerializer(many=False, required=True)
    ts2_default_tg = DimDmrTgSerializer(many=False, required=True)
    ts1_alternative_tgs = DimDmrTgSerializer(many=True, required=True)
    ts2_alternative_tgs = DimDmrTgSerializer(many=True, required=True)

    class Meta:
        model = DimDmr
        fields = "__all__"

    def create(self, validated_data):
        # Find and/or create the TGs
        tg = DimDmrTgSerializer().create(validated_data["tg"])
        ts1_default_tg = DimDmrTgSerializer().create(validated_data["ts1_default_tg"])
        ts2_default_tg = DimDmrTgSerializer().create(validated_data["ts2_default_tg"])
        ts1_alternative_tgs = [
            DimDmrTgSerializer().create(tg)
            for tg in validated_data["ts1_alternative_tgs"]
        ]
        ts2_alternative_tgs = [
            DimDmrTgSerializer().create(tg)
            for tg in validated_data["ts2_alternative_tgs"]
        ]
        ts_configuration = validated_data["ts_configuration"]
        color_code = validated_data["color_code"]

        # Find an object to update, or create a new one
        try:
            new_object = DimDmr.objects.get(tg__id=tg.id)
            new_object.ts1_default_tg = ts1_default_tg
            new_object.ts2_default_tg = ts2_default_tg
            new_object.color_code = color_code
        except DimDmr.DoesNotExist:
            new_object = DimDmr.objects.create(
                tg=tg,
                color_code=color_code,
                ts1_default_tg=ts1_default_tg,
                ts2_default_tg=ts2_default_tg,
            )
        new_object.ts_configuration = ts_configuration
        # https://stackoverflow.com/a/50015229/5168563
        for tg in ts1_alternative_tgs:
            new_object.ts1_alternative_tgs.add(tg)
        for tg in ts2_alternative_tgs:
            new_object.ts2_alternative_tgs.add(tg)
        new_object.save()
        return new_object


class DimTetraSerializer(  # pylint: disable=too-many-ancestors
    UniqueFieldsMixin, WritableNestedModelSerializer
):
    __doc__ = DimTetra.__doc__

    class Meta:
        model = DimTetra
        fields = "__all__"

    def create(self, validated_data):
        mcc = validated_data["mcc"]
        mnc = validated_data["mnc"]
        new_object, new_object_created = DimTetra.objects.get_or_create(
            mcc=mcc,
            mnc=mnc,
            defaults=validated_data,
        )
        if not new_object_created:
            new_object.save()
        return new_object


class DimLocationSerializer(UniqueFieldsMixin, serializers.ModelSerializer):
    __doc__ = DimLocation.__doc__

    class Meta:
        model = DimLocation
        fields = "__all__"

    def create(self, validated_data):
        latitude = validated_data.get("latitude", None)
        longitude = validated_data.get("longitude", None)
        if latitude is not None and longitude is not None:
            new_object, new_object_created = DimLocation.objects.get_or_create(
                latitude=latitude,
                longitude=longitude,
                defaults=validated_data,
            )
            if not new_object_created:
                new_object.region = validated_data["region"]
                new_object.place = validated_data["place"]
                new_object.qth_loc = validated_data["qth_loc"]
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
    info_holder = AssociationSerializer(many=False, required=False)
    info_location = DimLocationSerializer(many=False, required=False)

    class Meta:
        model = FactRepeater
        fields = "__all__"

from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers

from drf_writable_nested.serializers import WritableNestedModelSerializer
from drf_writable_nested.mixins import UniqueFieldsMixin

from utils.fields import HtmlRichTextSerializerField

from .models import (
    DimHalfDuplex,
    DimSimplex,
    DimFm,
    DimDStar,
    DimFusion,
    DimDmrTg,
    DimDmr,
    DimHolder,
    DimLocation,
    FactRepeater,
)


class DimHalfDuplexSerializer(UniqueFieldsMixin, serializers.ModelSerializer):
    shift = serializers.ReadOnlyField()

    class Meta:
        model = DimHalfDuplex
        fields = "__all__"

    def create(self, validated_data):
        tx_mhz = validated_data.get("tx_mhz", None)
        rx_mhz = validated_data.get("rx_mhz", None)
        channel = validated_data.get("channel", None)
        new_object, new_object_created = DimHalfDuplex.objects.get_or_create(
            tx_mhz=tx_mhz, rx_mhz=rx_mhz, defaults=validated_data
        )
        if not new_object_created and channel is not None:
            new_object.channel = channel
            new_object.save()
        return new_object


class DimSimplexSerializer(UniqueFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = DimSimplex
        fields = "__all__"

    def create(self, validated_data):
        freq_mhz = validated_data.get("freq_mhz", None)
        channel = validated_data.get("channel", None)
        new_object, new_object_created = DimSimplex.objects.get_or_create(
            freq_mhz=freq_mhz, defaults=validated_data
        )
        if not new_object_created and channel is not None:
            new_object.channel = channel
            new_object.save()
        return new_object


class DimFmSerializer(UniqueFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = DimFm
        fields = "__all__"

    def create(self, validated_data):
        modulation = validated_data.get("modulation", None)
        tone = validated_data.get("tone", None)
        if modulation is not None and tone is not None:
            new_object, _ = DimFm.objects.get_or_create(
                modulation=modulation, tone=tone, defaults=validated_data
            )
            return new_object
        return DimFm.objects.create(**validated_data)


class DimDStarSerializer(UniqueFieldsMixin, serializers.ModelSerializer):
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
    class Meta:
        model = DimDmrTg
        fields = "__all__"

    def create(self, validated_data):
        name = validated_data.get("name", None)
        dmr_id = validated_data.get("dmr_id", None)
        if dmr_id is not None:
            new_object, new_object_created = DimDmrTg.objects.get_or_create(
                dmr_id=dmr_id,
                defaults=validated_data,
            )
            if not new_object_created:
                new_object.name = name
                new_object.save()
            return new_object
        return DimDmrTg.objects.create(**validated_data)


class DimDmrSerializer(UniqueFieldsMixin, WritableNestedModelSerializer):
    ts1_default_tg = DimDmrTgSerializer(many=False, required=False)
    ts2_default_tg = DimDmrTgSerializer(many=False, required=False)
    ts1_alternative_tgs = DimDmrTgSerializer(many=True, required=False)
    ts2_alternative_tgs = DimDmrTgSerializer(many=True, required=False)
    ts_configuration = HtmlRichTextSerializerField(required=False)

    class Meta:
        model = DimDmr
        fields = "__all__"

    def create(self, validated_data):
        try:
            return DimDmr.objects.get(dmr_id=validated_data["dmr_id"])
        except ObjectDoesNotExist:
            return super(DimDmrSerializer, self).create(validated_data)


class DimHolderSerializer(UniqueFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = DimHolder
        fields = "__all__"

    def create(self, validated_data):
        abrv = validated_data.get("abrv", None)
        name = validated_data.get("name", None)
        sysop = validated_data.get("sysop", None)
        if abrv is not None:
            new_object, new_object_created = DimHolder.objects.get_or_create(
                abrv=abrv,
                defaults=validated_data,
            )
            if not new_object_created:
                if name is not None:
                    new_object.name = name
                if sysop is not None:
                    new_object.sysop = sysop
                new_object.save()
            return new_object
        return DimHolder.objects.create(**validated_data)


class DimLocationSerializer(UniqueFieldsMixin, serializers.ModelSerializer):
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


class FactRepeaterSerializer(WritableNestedModelSerializer):
    notes = HtmlRichTextSerializerField(required=False)

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

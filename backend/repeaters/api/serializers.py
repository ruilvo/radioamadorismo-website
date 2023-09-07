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
    DimDstar,
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

    def update(self, instance: DimRf, validated_data):
        instance.tx_mhz = validated_data.get("tx_mhz", instance.tx_mhz)
        instance.rx_mhz = validated_data.get("rx_mhz", instance.rx_mhz)
        instance.channel = validated_data.get("channel", instance.channel)
        instance.save()
        return instance

    def create(self, validated_data):
        """
        Even on create, recycles existing objects if they exist.
        """
        tx_mhz = validated_data["tx_mhz"]
        rx_mhz = validated_data["rx_mhz"]
        instance, instance_created = DimRf.objects.get_or_create(
            tx_mhz=tx_mhz, rx_mhz=rx_mhz, defaults=validated_data
        )
        if instance_created:
            return instance
        return self.update(instance, validated_data)


class DimFmSerializer(UniqueFieldsMixin, serializers.ModelSerializer):
    __doc__ = DimFm.__doc__

    class Meta:
        model = DimFm
        fields = "__all__"

    def update(self, instance: DimFm, validated_data):
        instance.modulation = validated_data.get("modulation", instance.modulation)
        instance.ctcss = validated_data.get("ctcss", instance.ctcss)
        instance.ctcss_sql = validated_data.get("ctcss_sql", instance.ctcss_sql)
        instance.bandwidth = validated_data.get("bandwidth", instance.bandwidth)
        instance.save()
        return instance

    def create(self, validated_data):
        """
        If this combination exists, don't create it.
        If it doesn't exist, create it.
        """
        instance, _ = DimFm.objects.get_or_create(
            **validated_data,
            defaults=validated_data,
        )
        return instance


class DimDstarSerializer(UniqueFieldsMixin, serializers.ModelSerializer):
    __doc__ = DimDstar.__doc__

    class Meta:
        model = DimDstar
        fields = "__all__"

    def update(self, instance: DimDstar, validated_data):
        instance.gateway = validated_data.get("gateway", instance.gateway)
        instance.reflector = validated_data.get("reflector", instance.reflector)
        instance.save()
        return instance

    def create(self, validated_data):
        """
        If this combination exists, don't create it.
        If it doesn't exist, create it.
        """
        instance, _ = DimDstar.objects.get_or_create(
            **validated_data,
            defaults=validated_data,
        )
        return instance


class DimFusionSerializer(UniqueFieldsMixin, serializers.ModelSerializer):
    __doc__ = DimFusion.__doc__

    class Meta:
        model = DimFusion
        fields = "__all__"

    def update(self, instance: DimFusion, validated_data):
        instance.wiresx = validated_data.get("wiresx", instance.wiresx)
        instance.room_id = validated_data.get("room_id", instance.room_id)
        instance.save()
        return instance

    def create(self, validated_data):
        """
        If this combination exists, don't create it.
        If it doesn't exist, create it.
        """
        instance, _ = DimFusion.objects.get_or_create(
            **validated_data,
            defaults=validated_data,
        )
        return instance


class DimDmrTgSerializer(UniqueFieldsMixin, serializers.ModelSerializer):
    __doc__ = DimDmrTg.__doc__

    class Meta:
        model = DimDmrTg
        fields = "__all__"

    def update(self, instance: DimDmrTg, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.call_mode = validated_data.get("call_mode", instance.call_mode)
        instance.save()
        return instance

    def create(self, validated_data):
        """
        If the ID exists, update it.
        If it doesn't exist, create it.
        """
        instance_id = validated_data["id"]
        instance, instance_created = DimDmrTg.objects.get_or_create(
            id=instance_id,
            defaults=validated_data,
        )
        if instance_created:
            return instance
        return self.update(instance, validated_data)


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


class DimTetraSerializer(  # pylint: disable=too-many-ancestors
    UniqueFieldsMixin, WritableNestedModelSerializer
):
    __doc__ = DimTetra.__doc__

    class Meta:
        model = DimTetra
        fields = "__all__"

    def update(self, instance: DimTetra, validated_data):
        instance.mcc = validated_data.get("mcc", instance.mcc)
        instance.mnc = validated_data.get("mnc", instance.mnc)
        instance.save()
        return instance

    def create(self, validated_data):
        """
        If this combination exists, don't create it.
        If it doesn't exist, create it.
        """
        instance, _ = DimTetra.objects.get_or_create(
            **validated_data,
            defaults=validated_data,
        )
        return instance


class DimLocationSerializer(UniqueFieldsMixin, serializers.ModelSerializer):
    __doc__ = DimLocation.__doc__

    class Meta:
        model = DimLocation
        fields = "__all__"

    def update(self, instance: DimLocation, validated_data):
        instance.latitude = validated_data.get("latitude", instance.latitude)
        instance.longitude = validated_data.get("longitude", instance.longitude)
        instance.region = validated_data.get("region", instance.region)
        instance.place = validated_data.get("place", instance.place)
        instance.save()
        return instance

    def create(self, validated_data):
        """
        If the latitude and longitude exist, update it.
        If it doesn't exist, create it.
        """
        latitude = validated_data.get("latitude", None)
        longitude = validated_data.get("longitude", None)
        if latitude is not None and longitude is not None:
            instance, instance_created = DimLocation.objects.get_or_create(
                latitude=latitude,
                longitude=longitude,
                defaults=validated_data,
            )
            if instance_created:
                return instance
            return self.update(instance, validated_data)
        # If latitude or longitude are not provided, create a new object to store the bad
        # data.
        return DimLocation.objects.create(**validated_data)


class FactRepeaterSerializer(  # pylint: disable=too-many-ancestors
    WritableNestedModelSerializer
):
    __doc__ = FactRepeater.__doc__

    info_rf = DimRfSerializer(many=False, required=False)
    info_fm = DimFmSerializer(many=False, required=False)
    info_dstar = DimDstarSerializer(many=False, required=False)
    info_fusion = DimFusionSerializer(many=False, required=False)
    info_dmr = DimDmrSerializer(many=False, required=False)
    info_holder = AssociationSerializer(many=False, required=False)
    info_location = DimLocationSerializer(many=False, required=False)
    info_tetra = DimTetraSerializer(many=False, required=False)

    class Meta:
        model = FactRepeater
        fields = "__all__"

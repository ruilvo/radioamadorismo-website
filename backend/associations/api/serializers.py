"""
Serializers for the associations API.
"""

from rest_framework import serializers

from drf_writable_nested.mixins import UniqueFieldsMixin

from associations.models import Association


class AssociationSerializer(UniqueFieldsMixin, serializers.ModelSerializer):
    __doc__ = Association.__doc__

    class Meta:
        model = Association
        fields = "__all__"

    def create(self, validated_data):
        abrv = validated_data["abrv"]
        new_object, new_object_created = Association.objects.get_or_create(
            abrv=abrv,
            defaults=validated_data,
        )
        if not new_object_created:
            new_object.name = validated_data["name"]
            new_object.email = validated_data["email"]
            new_object.website = validated_data["website"]
            new_object.notes = validated_data["notes"]
            new_object.save()
        return new_object

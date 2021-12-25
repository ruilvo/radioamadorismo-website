from rest_framework import serializers

from wagtail.embeds.models import Embed

from wagtailmedia.models import get_media_model

CURRENT_WAGTAIL_MEDIA_MODEL = get_media_model()


class WagtailMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CURRENT_WAGTAIL_MEDIA_MODEL
        fields = "__all__"


class WagtailEmbedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Embed
        fields = "__all__"

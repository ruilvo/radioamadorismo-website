from rest_framework import serializers

from wagtail.core.rich_text import expand_db_html


class HtmlRichTextSerializer(serializers.CharField):
    def to_representation(self, value):
        representation = super().to_representation(value)
        return expand_db_html(representation)

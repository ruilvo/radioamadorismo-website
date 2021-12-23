"""
https://github.com/wagtail/wagtail/issues/2695
"""

from rest_framework import serializers

from wagtail.api.conf import APIField
from wagtail.core.rich_text import expand_db_html


class HtmlRichTextSerializerField(serializers.CharField):
    def to_representation(self, value):
        representation = super().to_representation(value)
        return expand_db_html(representation)


class HtmlRichTextFieldApiField(APIField):
    def __init__(self, name):
        serializer = HtmlRichTextSerializerField()
        super().__init__(name=name, serializer=serializer)

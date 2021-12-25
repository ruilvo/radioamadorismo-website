from wagtail.core import blocks
from wagtail.embeds.blocks import EmbedBlock
from wagtail.core.rich_text import expand_db_html


class HtmlRichTextBlock(blocks.RichTextBlock):
    def get_api_representation(self, value, context=None):
        representation = super().get_api_representation(value, context)
        return expand_db_html(representation)


class BetterEmbedBlock(EmbedBlock):
    def get_api_representation(self, value, context=None):
        """
        Replaces `"value": <url>` with `"value": <html>`
        """
        return str(value)

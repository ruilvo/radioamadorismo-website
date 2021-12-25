from django.db import models
from django.utils.timezone import now

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField, StreamField
from wagtail.search import index
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.api import APIField

from wagtailmedia.blocks import AudioChooserBlock, VideoChooserBlock

from utils.fields import HtmlRichTextFieldApiField
from utils.blocks import HtmlRichTextBlock, BetterEmbedBlock


class BlogIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [FieldPanel("intro", classname="full")]

    api_fields = [
        APIField("intro"),
    ]


class BlogPage(Page):
    date = models.DateTimeField("Post date", default=now)
    intro = RichTextField()
    body = StreamField(
        [
            ("paragraph", HtmlRichTextBlock()),
            ("image", ImageChooserBlock(required=False)),
            ("document", DocumentChooserBlock(required=False)),
            ("embed", BetterEmbedBlock(required=False)),
            ("audio", AudioChooserBlock(icon="media", required=False)),
            ("video", VideoChooserBlock(icon="media", required=False)),
        ]
    )

    search_fields = Page.search_fields + [
        index.SearchField("intro"),
    ]

    content_panels = Page.content_panels + [
        FieldPanel("date"),
        FieldPanel("intro", classname="full"),
        StreamFieldPanel("body"),
    ]

    api_fields = [
        APIField("date"),
        HtmlRichTextFieldApiField("intro"),
        APIField("body"),
    ]

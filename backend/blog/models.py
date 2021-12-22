from django.db import models
from django.utils.timezone import now

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.search import index
from wagtail.api import APIField

from utils.fields import HtmlRichTextFieldApiField


class BlogIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [FieldPanel("intro", classname="full")]

    api_fields = [
        APIField("intro"),
    ]


class BlogPage(Page):
    date = models.DateTimeField("Post date", default=now)
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)

    search_fields = Page.search_fields + [
        index.SearchField("intro"),
        index.SearchField("body"),
    ]

    content_panels = Page.content_panels + [
        FieldPanel("date"),
        FieldPanel("intro"),
        FieldPanel("body", classname="full"),
    ]

    api_fields = [
        APIField("date"),
        APIField("intro"),
        HtmlRichTextFieldApiField("body"),
    ]

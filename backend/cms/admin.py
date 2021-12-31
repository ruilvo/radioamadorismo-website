from django.contrib import admin

from .models import (
    FactPdf,
    FactImage,
    FactBlogPost,
)

admin.site.register(FactPdf)
admin.site.register(FactImage)
admin.site.register(FactBlogPost)

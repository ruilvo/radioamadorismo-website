from django.contrib import admin

from .models import (
    FactPdf,
    FactAudio,
    FactImage,
    FactBlogPost,
)

admin.site.register(FactPdf)
admin.site.register(FactAudio)
admin.site.register(FactImage)
admin.site.register(FactBlogPost)

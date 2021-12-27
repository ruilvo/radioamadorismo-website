from django.contrib import admin

from .models import (
    FactImage,
    FactBlogPost,
)

admin.site.register(FactImage)
admin.site.register(FactBlogPost)

"""
Admin interface for the associations app.
"""

from django.contrib import admin

from associations.models import Association


class AssociationAdmin(admin.ModelAdmin):
    """
    Admin interface for the Association model.
    """

    save_as = True
    # inlines = (FactRepeaterInline,)
    list_display = (
        "id",
        "abrv",
        "name",
    )
    search_fields = (
        "id",
        "abrv",
        "name",
    )
    ordering = (
        "abrv",
        "name",
        "id",
    )


admin.site.register(Association, AssociationAdmin)

"""
Admin interface for the associations app.
"""

from django.contrib import admin

from repeaters.admin import FactRepeaterInline

from associations.models import Association


@admin.register(Association)
class AssociationAdmin(admin.ModelAdmin):
    """
    Admin interface for the Association model.
    """

    save_as = True
    save_on_top = True
    inlines = (FactRepeaterInline,)
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

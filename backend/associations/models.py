"""
Models for the associations app.
"""

from django.db import models

PLACEHOLDER_STR = "-----"


class Association(models.Model):
    """
    Models enough information for describing a ham radio association.
    """

    abrv = models.CharField(max_length=16, verbose_name="abrv.", unique=True)
    name = models.CharField(max_length=512, blank=True, verbose_name="name")
    email = models.EmailField(blank=True, verbose_name="e-mail")
    website = models.URLField(blank=True, verbose_name="website")
    notes = models.TextField(blank=True, verbose_name="notes")

    def __str__(self) -> str:
        return f"{self.abrv}: {self.name if self.name else PLACEHOLDER_STR}"

    class Meta:
        verbose_name = "Association"
        verbose_name_plural = "Associations"

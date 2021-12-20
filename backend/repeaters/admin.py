from django.contrib import admin
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import (
    DimHalfDuplex,
    DimSimplex,
    DimFm,
    DimDStar,
    DimFusion,
    DimDmr,
    DimHolder,
    DimLocation,
    FactRepeater,
)


class DimDmrAdminForm(forms.ModelForm):
    ts1_configuration = forms.CharField(widget=CKEditorUploadingWidget())
    ts2_configuration = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = DimDmr
        fields = "__all__"


class DimDmrAdmin(admin.ModelAdmin):
    form = DimDmrAdminForm


class FactRepeaterAdminForm(forms.ModelForm):
    notes = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = FactRepeater
        fields = "__all__"


class FactRepeaterAdmin(admin.ModelAdmin):
    form = FactRepeaterAdminForm


# Register your models here.
admin.site.register(DimHalfDuplex)
admin.site.register(DimSimplex)
admin.site.register(DimFm)
admin.site.register(DimDStar)
admin.site.register(DimFusion)
admin.site.register(DimDmr, DimDmrAdmin)
admin.site.register(DimHolder)
admin.site.register(DimLocation)
admin.site.register(FactRepeater, FactRepeaterAdmin)

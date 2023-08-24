# Generated by Django 4.2.4 on 2023-08-24 12:43

from django.db import migrations

from django.contrib.gis.geos import Point


def combine_names(apps, _):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    DimLocation = apps.get_model("repeaters", "DimLocation")
    for location in DimLocation.objects.all():
        lat = float(location.latitude) if location.latitude is not None else 0.0
        long = float(location.longitude) if location.longitude is not None else 0.0
        loc = Point(long, lat)
        location.location = loc
        location.save()


class Migration(migrations.Migration):
    dependencies = [
        ("repeaters", "0002_dimlocation_location"),
    ]

    operations = []

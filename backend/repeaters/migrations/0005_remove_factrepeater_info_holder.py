# Generated by Django 4.2.4 on 2023-08-24 17:30

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("repeaters", "0004_factrepeater_add_temp_associations"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="factrepeater",
            name="info_holder",
        ),
    ]

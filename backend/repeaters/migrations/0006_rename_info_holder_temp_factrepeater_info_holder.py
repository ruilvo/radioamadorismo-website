# Generated by Django 4.2.4 on 2023-08-24 17:31

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("repeaters", "0005_remove_factrepeater_info_holder"),
    ]

    operations = [
        migrations.RenameField(
            model_name="factrepeater",
            old_name="info_holder_temp",
            new_name="info_holder",
        ),
    ]

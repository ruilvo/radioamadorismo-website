# Generated by Django 4.2.2 on 2023-06-24 09:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("repeaters", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="dimdmrtg",
            name="call_mode",
            field=models.CharField(
                choices=[
                    ("GROUP_CALL", "Group Call"),
                    ("PRIVATE_CALL", "Private Call"),
                ],
                default="GROUP_CALL",
                max_length=50,
                verbose_name="call mode",
            ),
        ),
    ]

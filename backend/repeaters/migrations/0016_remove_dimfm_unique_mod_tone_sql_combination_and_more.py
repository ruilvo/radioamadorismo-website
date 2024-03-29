# Generated by Django 4.2.5 on 2023-09-07 07:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("repeaters", "0015_alter_dimfm_ctcss"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="dimfm",
            name="unique mod./tone/SQL combination",
        ),
        migrations.RenameField(
            model_name="dimfm",
            old_name="tone_sql",
            new_name="ctcss_sql",
        ),
        migrations.AddConstraint(
            model_name="dimfm",
            constraint=models.UniqueConstraint(
                fields=("modulation", "ctcss", "ctcss_sql"),
                name="unique mod./tone/SQL combination",
            ),
        ),
    ]

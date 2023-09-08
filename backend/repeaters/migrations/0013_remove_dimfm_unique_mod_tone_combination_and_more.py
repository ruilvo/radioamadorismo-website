# Generated by Django 4.2.5 on 2023-09-07 06:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("repeaters", "0012_alter_dimlocation_qth_loc"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="dimfm",
            name="unique mod./tone combination",
        ),
        migrations.AddField(
            model_name="dimfm",
            name="tone_sql",
            field=models.BooleanField(default=False, verbose_name="tone SQL"),
        ),
        migrations.AddConstraint(
            model_name="dimfm",
            constraint=models.UniqueConstraint(
                fields=("modulation", "tone", "tone_sql"),
                name="unique mod./tone/SQL combination",
            ),
        ),
    ]
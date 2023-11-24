from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("repeaters", "0020_remove_dimdmr_ts1_default_tg_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="dimdmr",
            old_name="ts1_alternative_tgs",
            new_name="ts1_tgs",
        ),
        migrations.RenameField(
            model_name="dimdmr",
            old_name="ts2_alternative_tgs",
            new_name="ts2_tgs",
        ),
    ]

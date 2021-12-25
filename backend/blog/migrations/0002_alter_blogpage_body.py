# Generated by Django 3.2.10 on 2021-12-25 10:52

from django.db import migrations
import utils.blocks
import wagtail.core.fields
import wagtail.documents.blocks
import wagtail.images.blocks
import wagtailmedia.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpage',
            name='body',
            field=wagtail.core.fields.StreamField([('paragraph', utils.blocks.HtmlRichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock(required=False)), ('document', wagtail.documents.blocks.DocumentChooserBlock(required=False)), ('embed', utils.blocks.BetterEmbedBlock(required=False)), ('audio', wagtailmedia.blocks.AudioChooserBlock(icon='media', required=False)), ('video', wagtailmedia.blocks.VideoChooserBlock(icon='media', required=False))]),
        ),
    ]

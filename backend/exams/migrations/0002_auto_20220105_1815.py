# Generated by Django 3.2.10 on 2022-01-05 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='factexamquestion',
            name='question_image_height',
        ),
        migrations.RemoveField(
            model_name='factexamquestion',
            name='question_image_width',
        ),
        migrations.AlterField(
            model_name='factexamquestion',
            name='question_image',
            field=models.ImageField(blank=True, max_length=255, null=True, upload_to='exams/%Y/%m/'),
        ),
    ]

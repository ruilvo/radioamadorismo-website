# Generated by Django 3.2.10 on 2022-01-05 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FactExamQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField()),
                ('answer_a', models.TextField()),
                ('answer_b', models.TextField()),
                ('answer_c', models.TextField()),
                ('answer_d', models.TextField()),
                ('correct_answer', models.CharField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')], max_length=1)),
                ('category', models.CharField(choices=[('1', 'Category 1'), ('2', 'Category 2'), ('2', 'Category 3')], max_length=5)),
                ('question_image_width', models.PositiveIntegerField(editable=False)),
                ('question_image_height', models.PositiveIntegerField(editable=False)),
                ('question_image', models.ImageField(blank=True, height_field='question_image_height', max_length=255, null=True, upload_to='exams/%Y/%m/', width_field='question_image_width')),
            ],
            options={
                'verbose_name': 'exam question',
                'verbose_name_plural': 'exam questions',
            },
        ),
    ]

# Generated by Django 5.1.6 on 2025-02-19 22:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizzes', '0006_category_featured_quiz_featured'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='cateogry_featured',
            field=models.BooleanField(default=False),
        ),
    ]

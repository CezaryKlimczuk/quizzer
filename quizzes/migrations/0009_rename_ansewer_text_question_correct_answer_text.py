# Generated by Django 5.1.6 on 2025-02-22 23:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quizzes', '0008_rename_cateogry_featured_quiz_category_featured'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='ansewer_text',
            new_name='correct_answer_text',
        ),
    ]

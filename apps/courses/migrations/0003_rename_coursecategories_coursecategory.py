# Generated by Django 5.2.3 on 2025-07-07 09:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_rename_categories_category_rename_courses_course'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CourseCategories',
            new_name='CourseCategory',
        ),
    ]

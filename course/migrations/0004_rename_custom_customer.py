# Generated by Django 5.1.1 on 2024-09-13 13:54

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0003_alter_comment_video_id_alter_course_category_id_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Custom',
            new_name='Customer',
        ),
    ]
# Generated by Django 5.1.1 on 2024-09-13 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0004_rename_custom_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='phone',
            field=models.CharField(max_length=20),
        ),
    ]
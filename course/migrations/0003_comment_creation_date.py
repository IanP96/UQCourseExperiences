# Generated by Django 5.0 on 2024-01-02 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0002_experience_creation_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='creation_date',
            field=models.DateField(auto_now=True),
        ),
    ]

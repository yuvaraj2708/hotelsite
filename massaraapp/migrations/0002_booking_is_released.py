# Generated by Django 5.0.1 on 2024-01-08 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('massaraapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='is_released',
            field=models.BooleanField(default=False),
        ),
    ]

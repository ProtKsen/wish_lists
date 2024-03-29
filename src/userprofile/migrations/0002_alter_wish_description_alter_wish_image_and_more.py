# Generated by Django 4.1.7 on 2023-04-01 11:36

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("userprofile", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="wish",
            name="description",
            field=models.CharField(blank=True, default="", max_length=500),
        ),
        migrations.AlterField(
            model_name="wish",
            name="image",
            field=models.ImageField(
                blank=True,
                default="img/wish_default.jpg",
                upload_to="img/",
                validators=[
                    django.core.validators.FileExtensionValidator([".png", ".jpg", ".jpeg"])
                ],
            ),
        ),
        migrations.AlterField(
            model_name="wish",
            name="link",
            field=models.CharField(blank=True, default="", max_length=50),
        ),
        migrations.AlterField(
            model_name="wish",
            name="type",
            field=models.CharField(blank=True, default="Разное", max_length=50),
        ),
    ]

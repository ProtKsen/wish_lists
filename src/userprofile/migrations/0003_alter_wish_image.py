# Generated by Django 4.1.7 on 2023-04-01 15:47

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("userprofile", "0002_alter_wish_description_alter_wish_image_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="wish",
            name="image",
            field=models.ImageField(
                blank=True,
                default="img/wish_default.jpg",
                upload_to="img/",
                validators=[django.core.validators.validate_image_file_extension],
            ),
        ),
    ]

# Generated by Django 4.1.7 on 2023-03-10 04:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("friends", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="friendrequest",
            name="status",
            field=models.CharField(
                choices=[
                    ("Pending", "Pending"),
                    ("Accepted", "Accepted"),
                    ("Rejected", "Rejected"),
                ],
                default="PENDING",
                max_length=8,
            ),
        ),
    ]

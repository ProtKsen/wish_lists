# Generated by Django 4.1.7 on 2023-04-03 05:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("friends", "0002_alter_friendrequest_status"),
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
                default="Pending",
                max_length=8,
            ),
        ),
    ]

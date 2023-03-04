# Generated by Django 4.1.7 on 2023-03-04 11:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("schema", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Dataset",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "file",
                    models.FileField(blank=True, null=True, upload_to="datasets/"),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="datasets",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]

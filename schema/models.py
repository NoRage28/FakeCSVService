from django.db import models
from schema.choices import SCHEMA_STRING_CHARACTER, SCHEMA_COLUMN_SEPARATOR
from django.contrib.auth import get_user_model

User = get_user_model()


class Schema(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    column_separator = models.CharField(
        max_length=255,
        choices=SCHEMA_COLUMN_SEPARATOR,
        default=SCHEMA_COLUMN_SEPARATOR[0],
    )
    string_character = models.CharField(
        max_length=255,
        choices=SCHEMA_STRING_CHARACTER,
        default=SCHEMA_STRING_CHARACTER[0],
    )
    columns = models.JSONField(blank=False, null=False)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="schemas")

    def __str__(self):
        return self.name


class Dataset(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="datasets")
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to="datasets/", null=True, blank=True)

    def __str__(self):
        return self.name

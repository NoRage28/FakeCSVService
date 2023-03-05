from rest_framework.test import APITestCase
from rest_framework import status
from schema.models import Schema, Dataset
from django.contrib.auth.models import User
from django.urls import reverse
from django.test.utils import override_settings


class TestDataset(APITestCase):
    def setUp(self) -> None:
        self.columns_data = [
            {"name": "column_1", "type": "job"},
            {"name": "column_2", "type": "phone_number"},
            {"name": "column_3", "type": "integer", "value_from": 1, "value_to": 50},
        ]
        self.user = User.objects.create_user(
            username="test_user", password="1357246test"
        )
        self.schema = Schema.objects.create(
            user=self.user,
            name="Schema_1",
            column_separator=".",
            string_character='"',
            columns=self.columns_data,
        )

        self.client.force_authenticate(user=self.user)

    @override_settings(
        CELERY_TASK_EAGER_PROPAGATES=True,
        CELERY_TASK_ALWAYS_EAGER=True,
        BROKER_BACKEND="memory",
    )
    def test_create_dataset(self):
        url = reverse("schema-create_dataset", kwargs={"pk": self.schema.pk})
        data = {"name": "Schema_1", "rows": "100"}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Dataset.objects.all().count(), 1)
        self.assertEqual(Dataset.objects.last().name, 'Schema_1')

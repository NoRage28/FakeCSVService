from rest_framework.test import APITestCase
from rest_framework import status
from schema.models import Schema
from django.contrib.auth.models import User
from django.urls import reverse


class TestSchema(APITestCase):
    def setUp(self) -> None:
        self.columns_data = [{"name": "Column_1", "type": "job"}]
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

    def test_get_schema(self):
        url = reverse("schema-list")
        response = self.client.get(path=url)
        result = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(result, list)
        for key, value in result[0].items():
            if key == "updated_at":
                continue
            self.assertEqual(getattr(self.schema, key), value)

    def test_post_schema(self):
        url = reverse("schema-list")
        data = {
            "name": "Schema_2",
            "column_separator": ",",
            "string_character": "'",
            "columns": [
                {"name": "Column_1", "type": "integer", "value_from": 1, "value_to": 20}
            ],
        }
        response = self.client.post(path=url, data=data, format="json")
        created_schema = Schema.objects.last()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Schema.objects.all().count(), 2)
        for key, value in data.items():
            if key == "updated_at":
                continue
            self.assertEqual(getattr(created_schema, key), value)

    def test_update_schema(self):
        url = reverse("schema-detail", kwargs={"pk": self.schema.pk})
        data = {
            "name": "Schema_3",
            "column_separator": ",",
            "string_character": "'",
            "columns": [
                {"name": "Column_2", "type": "integer", "value_from": 1, "value_to": 50}
            ],
        }
        response = self.client.patch(path=url, data=data, format="json")
        updated_schema = Schema.objects.get(pk=self.schema.pk)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Schema.objects.all().count(), 1)
        for key, value in data.items():
            if key == "updated_at":
                continue
            self.assertEqual(getattr(updated_schema, key), value)

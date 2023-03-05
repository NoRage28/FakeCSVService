import csv
import os

from schema.models import Schema, Dataset
from schema.utils import create_file_name

from django.core.files import File
from typing import Dict, List, Optional, Any
from faker import Faker


class DatasetCreator:
    def __init__(self):
        self.fake_data_creator = FakeDataGeneratorService()
        self.file_writer = CSVFileWriter()
        self.file_name = create_file_name()

    def create_dataset(self, user_id: str, data: Dict, schema_pk: str):
        self._create_file_with_fake_data(data=data, schema_pk=schema_pk)
        self._save_dataset_file_to_db(user_id=user_id, data=data)
        self._remove_file_from_disk()

    def _create_file_with_fake_data(self, data: Dict, schema_pk: str):
        schema = Schema.objects.get(id=schema_pk)
        fake_data = self.fake_data_creator.generate_fake_data(
            schema_columns=schema.columns, number_of_rows=data.get("rows")
        )
        self.file_writer.write_data_to_file(
            file_name=self.file_name,
            data=fake_data,
            delimiter=schema.column_separator,
            quotechar=schema.string_character,
        )

    def _save_dataset_file_to_db(self, user_id: str, data: Dict):
        with open(f'{self.file_name}.csv', "r") as csv_file:
            Dataset.objects.create(
                user_id=user_id, name=data.get('name'), file=File(csv_file)
            )

    def _remove_file_from_disk(self):
        os.remove(f'{self.file_name}.csv')


class CSVFileWriter:
    def write_data_to_file(
        self, file_name: str, data: List[Dict], delimiter: str, quotechar: str
    ):
        to_csv = data
        keys = to_csv[0].keys()

        with open(f"{file_name}.csv", "w") as output_file:
            dict_writer = csv.DictWriter(
                output_file, keys, delimiter=delimiter, quotechar=quotechar
            )
            dict_writer.writeheader()
            dict_writer.writerows(to_csv)


class FakeDataGeneratorService:
    def __init__(self):
        self.faker = Faker()

    def generate_fake_data(self, schema_columns: List[Dict], number_of_rows: int):
        rows = []
        for _ in range(number_of_rows):
            row = {}
            for column in schema_columns:
                column_name = column.get("name")
                column_type = column.get("type")
                value_from = column.get("value_from")
                value_to = column.get("value_to")

                row[column_name] = self._generate_fake_value(
                    column_type=column_type, value_from=value_from, value_to=value_to
                )
            rows.append(row)

        return rows

    def _generate_fake_value(
        self, column_type: str, value_from: Optional[int], value_to: Optional[int]
    ) -> Any:
        column_type_to_faker_map = {
            "full_name": self.faker.name,
            "integer": self.faker.pyint,
            "job": self.faker.job,
            "phone_number": self.faker.phone_number,
            "email": self.faker.email,
        }

        func = column_type_to_faker_map.get(column_type)

        if column_type == "integer":
            return func(min_value=value_from, max_value=value_to)
        else:
            return func()




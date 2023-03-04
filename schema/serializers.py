from typing import Any, Dict
from rest_framework import serializers
from schema.choices import (
    SCHEMA_COLUMN_SEPARATOR,
    SCHEMA_COLUMN_TYPE,
    SCHEMA_STRING_CHARACTER,
)
from schema.models import Schema, Dataset


class SchemaColumnSerializer(serializers.Serializer):
    name = serializers.CharField()
    type = serializers.ChoiceField(choices=SCHEMA_COLUMN_TYPE)
    value_from = serializers.IntegerField(min_value=0, required=False)
    value_to = serializers.IntegerField(min_value=1, required=False)

    def validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        if not data["type"] == "integer":
            return data

        value_from = data.get("value_from")
        value_to = data.get("value_to")

        if None in (value_from, value_to):
            raise serializers.ValidationError(
                "Values 'from' and 'to' required with field with type 'integer'."
            )

        if value_from > value_to:
            raise serializers.ValidationError(
                "Value of field 'to' should be higher than value of field 'from'."
            )

        return data


class SchemaSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    name = serializers.CharField()
    column_separator = serializers.ChoiceField(choices=SCHEMA_COLUMN_SEPARATOR)
    string_character = serializers.ChoiceField(choices=SCHEMA_STRING_CHARACTER)
    columns = serializers.ListField(child=SchemaColumnSerializer(), allow_empty=False)

    class Meta:
        model = Schema
        fields = "__all__"


class DataSetSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    rows = serializers.IntegerField(min_value=1, required=False)

    class Meta:
        model = Dataset
        fields = "__all__"

    def validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        if not data.get("rows"):
            raise serializers.ValidationError("Value 'rows' required.")
        return data

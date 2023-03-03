from rest_framework import viewsets
from schema.models import Schema
from schema.serializers import SchemaSerializer


class SchemaViewSet(viewsets.ModelViewSet):
    queryset = Schema.objects.all()
    serializer_class = SchemaSerializer

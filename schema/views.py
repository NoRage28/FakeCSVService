from rest_framework import viewsets, views, status
from rest_framework.response import Response
from schema.models import Schema, Dataset
from schema.serializers import SchemaSerializer, DataSetSerializer
from rest_framework.decorators import action
from django.core.cache import cache

from schema.services import start_create_dataset_task


class SchemaViewSet(viewsets.ModelViewSet):
    queryset = Schema.objects.all()
    serializer_class = SchemaSerializer

    @action(detail=True, methods=["post"], url_name="create_dataset")
    def create_dataset(self, request, pk):
        serializer = DataSetSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        cache_task_key = start_create_dataset_task(
            user_id=request.user.pk, data=serializer.data, schema_pk=pk
        )

        return Response({'cache_task_key': cache_task_key}, status=status.HTTP_201_CREATED)


class DataSetViewSet(viewsets.ModelViewSet):
    queryset = Dataset.objects.all()
    serializer_class = DataSetSerializer




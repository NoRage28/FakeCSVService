from rest_framework import viewsets, views, status
from rest_framework.response import Response
from rest_framework import permissions
from schema.models import Schema, Dataset
from schema.serializers import SchemaSerializer, DataSetSerializer
from rest_framework.decorators import action
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from schema.tasks import start_create_dataset_task


class SchemaViewSet(viewsets.ModelViewSet):
    queryset = Schema.objects.all()
    serializer_class = SchemaSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=["post"], url_name="create_dataset")
    def create_dataset(self, request, pk):
        serializer = DataSetSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        cache_task_key = start_create_dataset_task(
            user_id=request.user.pk, data=serializer.data, schema_pk=pk
        )

        return Response(
            {"cache_task_key": cache_task_key}, status=status.HTTP_201_CREATED
        )


class DataSetViewSet(viewsets.ModelViewSet):
    queryset = Dataset.objects.all()
    serializer_class = DataSetSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=["get"], url_name="download_dataset")
    def download(self, request, pk):
        dataset = get_object_or_404(Dataset, id=pk)
        serializer = self.get_serializer(dataset)
        data = {
            "name": serializer.data.get("name"),
            "download_url": serializer.data.get("file"),
        }
        return Response(data=data, status=status.HTTP_200_OK)


class TaskStatusAPIView(views.APIView):
    def get(self, request, format=None):
        task_id = self.request.query_params["task_id"]
        task_status = cache.get(task_id)
        return Response(task_status, status=status.HTTP_200_OK)

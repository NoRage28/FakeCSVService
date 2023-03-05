from rest_framework.routers import DefaultRouter
from schema.views import SchemaViewSet, DataSetViewSet, TaskStatusAPIView
from django.urls import path

router = DefaultRouter()
router.register(r"schema", SchemaViewSet, basename="schema")
router.register(r"dataset", DataSetViewSet, basename="dataset")

urlpatterns = [path("status_task/", TaskStatusAPIView.as_view())]

urlpatterns += router.urls

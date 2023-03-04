from rest_framework.routers import DefaultRouter
from schema.views import SchemaViewSet, DataSetViewSet
from django.urls import path

router = DefaultRouter()
router.register(r"schema", SchemaViewSet, basename="schema")
router.register(r"dataset", DataSetViewSet, basename="dataset")

urlpatterns = []

urlpatterns += router.urls

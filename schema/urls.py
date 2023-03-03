from rest_framework.routers import DefaultRouter
from schema.views import SchemaViewSet

router = DefaultRouter()
router.register(r"schema", SchemaViewSet, basename="schema")

urlpatterns = []

urlpatterns += router.urls

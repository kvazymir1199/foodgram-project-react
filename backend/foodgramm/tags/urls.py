from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import TagViewSet

app_name = 'tags'
router = DefaultRouter()

router.register("tags", TagViewSet, basename="tags")

urlpatterns = [
    path(r'', include(router.urls)),
]

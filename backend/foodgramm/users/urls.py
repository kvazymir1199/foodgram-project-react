from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CustomUserViewSet

router = DefaultRouter()

router.register("users", CustomUserViewSet, basename="users")

urlpatterns = [
    path(r'', include(router.urls)),
]

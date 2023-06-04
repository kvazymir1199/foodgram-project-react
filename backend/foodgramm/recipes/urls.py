from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import RecipeViewSet

app_name = 'recipes'
router = DefaultRouter()


router.register("recipes", RecipeViewSet, basename="recipes")
urlpatterns = [
    path(r'', include(router.urls)),
]

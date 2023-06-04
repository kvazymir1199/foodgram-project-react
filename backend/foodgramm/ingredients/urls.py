from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import IngredientView

app_name = 'ingredients'
router = DefaultRouter()


router.register("ingredients", IngredientView, basename="ingredients")
urlpatterns = [
    path(r'', include(router.urls)),
]

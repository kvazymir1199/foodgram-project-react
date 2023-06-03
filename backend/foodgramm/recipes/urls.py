from foodgramm.router import DefaultRouter

from .views import RecipeViewSet

router = DefaultRouter()


router.register("recipes", RecipeViewSet, basename="recipes")

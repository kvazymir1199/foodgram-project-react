from foodgramm.router import DefaultRouter

from .views import IngredientView

router = DefaultRouter()


router.register("ingredients", IngredientView, basename="ingredients")

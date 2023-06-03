from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from .router import DefaultRouter

from ingredients.views import IngredientView
from recipes.views import RecipeViewSet
from tags.views import TagViewSet
from users.views import CustomUserViewSet
from ingredients.urls import router as ingredients_router
from recipes.urls import router as recipes_router
from tags.urls import router as tag_router
from users.urls import router as users_router

router = DefaultRouter()

router.extend(ingredients_router)
router.extend(tag_router)
router.extend(recipes_router)
router.extend(users_router)
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/auth/", include("djoser.urls.authtoken")),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

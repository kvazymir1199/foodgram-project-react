from foodgramm.router import DefaultRouter

from .views import TagViewSet

router = DefaultRouter()

router.register("tags", TagViewSet, basename="tags")

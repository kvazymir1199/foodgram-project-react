from foodgramm.router import DefaultRouter

from .views import UserViewSet

router = DefaultRouter()

router.register("users", UserViewSet, basename="users")
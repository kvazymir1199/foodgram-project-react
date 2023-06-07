from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

apps_patterns = [
    path('', include(('users.urls', 'users'), namespace='users')),
    path('', include(('recipes.urls', 'recips'), namespace='recipes')),
    path('', include(
        ('ingredients.urls', 'ingredients'),
        namespace='ingredients')),
    path('', include(('tags.urls', 'tags'), namespace='tags')),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(apps_patterns)),
    path("api/auth/", include("djoser.urls.authtoken")),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT)



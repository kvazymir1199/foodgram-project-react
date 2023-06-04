from django.urls import include, path

app_name = 'api'
api_patterns = [
    path('', include(('users.urls', 'users'), namespace='api_users')),
    path('', include(('recipes.urls', 'recips'), namespace='api_recipes')),
    path('', include(
        ('ingredients.urls', 'ingredients'),
        namespace='api_ingredients')),
    path('', include(('tags.urls', 'tags'), namespace='api_tags')),
]

urlpatterns = [
    path("", include(api_patterns)),
]

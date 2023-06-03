from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Recipe)
admin.site.register(IngredientsForRecipe)
admin.site.register(TagForRecipe)
admin.site.register(FavoriteRecipe)
admin.site.register(ShopingCard)

from django.contrib import admin


from .models import (
    Recipe,
    IngredientsForRecipe,
    TagForRecipe,
    FavoriteRecipe,
    ShopingCard)

admin.site.register(Recipe)
admin.site.register(IngredientsForRecipe)
admin.site.register(TagForRecipe)
admin.site.register(FavoriteRecipe)
admin.site.register(ShopingCard)

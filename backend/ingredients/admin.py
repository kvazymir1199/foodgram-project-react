from django.contrib import admin

# Register your models here.
from .models import Ingredient, IngredientForRecipe

admin.site.register(Ingredient)
admin.site.register(IngredientForRecipe)

from rest_framework import serializers

from .models import Ingredient, IngredientForRecipe


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = "__all__"


class IngredientForRecipeSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer()

    class Meta:
        model = IngredientForRecipe
        fields = "__all__"



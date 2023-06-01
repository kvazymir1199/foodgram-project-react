from django.shortcuts import get_object_or_404
from rest_framework import serializers
from .models import *
from ingredients.serializers import IngredientSerializer
from tags.serializers import TagSerializer
from django.contrib.auth import get_user_model
from django.core import exceptions
import base64

from django.core.files.base import ContentFile

User = get_user_model()


class RecipeIngredientsSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField(method_name="get_id")
    name = serializers.SerializerMethodField(method_name="get_name")
    measurement_unit = serializers.SerializerMethodField(
        method_name="get_measurement_unit"
    )

    def get_id(self, obj):
        print(obj)
        return obj.ingredient.id

    def get_name(self, obj):
        return obj.ingredient.name

    def get_measurement_unit(self, obj):
        return obj.ingredient.measurement_unit

    class Meta:
        model = IngredientsForRecipe
        fields = ("id", "name", "measurement_unit", "amount")


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
        )


class CreateUpdateRecipeIngredientsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    amount = serializers.IntegerField(
        validators=[
            MinValueValidator(1),
        ]
    )

    class Meta:
        model = Ingredient
        fields = ("id", "amount")


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = serializers.SerializerMethodField(method_name="get_ingredients")
    tags = TagSerializer(many=True)
    author = CustomUserSerializer()

    class Meta:
        model = Recipe
        # fields = ("id", "author", "ingredients", "name", "tags")
        fields = "__all__"

    def get_ingredients(self, obj):
        ingredients = IngredientsForRecipe.objects.filter(recipe=obj)
        serializer = RecipeIngredientsSerializer(ingredients, many=True)
        return serializer.data


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        # Если полученный объект строка, и эта строка
        # начинается с 'data:image'...
        if isinstance(data, str) and data.startswith("data:image"):
            # ...начинаем декодировать изображение из base64.
            # Сначала нужно разделить строку на части.
            format, imgstr = data.split(";base64,")
            # И извлечь расширение файла.
            ext = format.split("/")[-1]
            # Затем декодировать сами данные и поместить результат в файл,
            # которому дать название по шаблону.
            data = ContentFile(base64.b64decode(imgstr), name="temp." + ext)

        return super().to_internal_value(data)


class RecipeCreateUpdateSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True)
    ingredients = CreateUpdateRecipeIngredientsSerializer(many=True)
    image = Base64ImageField()
    cooking_time = serializers.IntegerField(
        validators=(
            MinValueValidator(
                1, message="Время приготовления должно быть 1 или более."
            ),
        )
    )

    def validate_tags(self, value):
        if not value:
            raise exceptions.ValidationError("Нужно добавить хотя бы один тег.")

        return value

    def validate_ingredients(self, value):
        if not value:
            raise exceptions.ValidationError("Нужно добавить хотя бы один ингредиент.")

        ingredients = [item["id"] for item in value]
        for ingredient in ingredients:
            if ingredients.count(ingredient) > 1:
                raise exceptions.ValidationError(
                    "У рецепта не может быть два одинаковых ингредиента."
                )

        return value

    def create(self, validated_data):
        author = self.context.get("request").user
        tags = validated_data.pop("tags")
        ingredients = validated_data.pop("ingredients")

        recipe = Recipe.objects.create(author=author, **validated_data)
        recipe.tags.set(tags)

        for ingredient in ingredients:
            amount = ingredient["amount"]
            ingredient = get_object_or_404(Ingredient, pk=ingredient["id"])

            IngredientsForRecipe.objects.create(
                recipe=recipe, ingredient=ingredient, amount=amount
            )

        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.pop("tags", None)
        if tags is not None:
            instance.tags.set(tags)

        ingredients = validated_data.pop("ingredients", None)
        if ingredients is not None:
            instance.ingredients.clear()

            for ingredient in ingredients:
                amount = ingredient["amount"]
                ingredient = get_object_or_404(Ingredient, pk=ingredient["id"])

                IngredientsForRecipe.objects.update_or_create(
                    recipe=instance, ingredient=ingredient, defaults={"amount": amount}
                )

        return super().update(instance, validated_data)

    def to_representation(self, instance):
        serializer = RecipeSerializer(
            instance, context={"request": self.context.get("request")}
        )

        return serializer.data

    class Meta:
        model = Recipe
        fields = "__all__"


class ShortRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ("id", "name", "image", "cooking_time")

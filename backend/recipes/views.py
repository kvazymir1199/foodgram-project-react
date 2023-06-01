from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import exceptions, status, viewsets
from rest_framework.decorators import action
from django.db.models import Sum

# Create your views here.

from .models import IngredientsForRecipe, Recipe
from .serializers import (
    RecipeSerializer,
    RecipeCreateUpdateSerializer,
    ShortRecipeSerializer,
)
from .models import FavoriteRecipe, ShopingCard
from ingredients.models import Ingredient


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()

    def get_serializer_class(self):
        if self.request.method in ("POST", "PATCH"):
            return RecipeCreateUpdateSerializer
        return RecipeSerializer

    @action(detail=True, methods=("post", "delete"))
    def favorite(self, request, pk=None):
        user = self.request.user
        recipe = get_object_or_404(Recipe, id=pk)
        check = FavoriteRecipe.objects.filter(user=user).exists()
        if self.request.method == "DELETE":
            if not check:
                raise exceptions.ValidationError("Рецепта в избранном нет")
            favorite = get_object_or_404(FavoriteRecipe, user=user, recipe=recipe)
            # favorite = FavoriteRecipe.objects.filter(user=user, recipe=recipe)
            favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        if self.request.method == "POST":
            if check:
                raise exceptions.ValidationError("Рецепт уже в избранном")
            FavoriteRecipe.objects.create(user=user, recipe=recipe)
            serializer = RecipeSerializer(recipe, context={"request": request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(detail=True, methods=("post", "delete"))
    def shopingcard(self, request, pk=None):
        user = self.request.user
        recipe = get_object_or_404(Recipe, id=pk)
        check = ShopingCard.objects.filter(user=user).exists()
        if self.request.method == "DELETE":
            if not check:
                raise exceptions.ValidationError(f"Рецепта {pk} нет в корзине")
            favorite = get_object_or_404(ShopingCard, user=user, recipe=recipe)
            favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        if self.request.method == "POST":
            if check:
                raise exceptions.ValidationError(f"Рецепт {pk} уже у вас в корзине")
            ShopingCard.objects.create(user=user, recipe=recipe)
            serializer = ShortRecipeSerializer(recipe, context={"request": request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    # @action(detail=True, methods=("post"))
    # def download_shoping_card(self,request,pk=None):
    #     pass
    @action(detail=False, methods=("get",))
    def download_shopping_cart(self, request):
        shopping_cart = ShopingCard.objects.filter(user=self.request.user)
        recipes = [item.recipe.id for item in shopping_cart]
        buy_list = (
            IngredientsForRecipe.objects.filter(recipe__in=recipes)
            .values("ingredient")
            .annotate(amount=Sum("amount"))
        )

        buy_list_text = "Список покупок с сайта Foodgram:\n\n"
        for item in buy_list:
            ingredient = Ingredient.objects.get(pk=item["ingredient"])
            amount = item["amount"]
            buy_list_text += (
                f"{ingredient.name}, {amount} " f"{ingredient.measurement_unit}\n"
            )

        response = HttpResponse(buy_list_text, content_type="text/plain")
        response["Content-Disposition"] = "attachment; filename=shopping-list.txt"

        return response

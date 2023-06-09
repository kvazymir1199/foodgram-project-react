from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .filters import RecipeFilter
from .models import FavoriteRecipe, IngredientsForRecipe, Recipe, ShopingCard
from .pagination import RecipeViewSetPagination
from .pdf2html import get_pdf_file

from .serializers import (RecipeCreateUpdateSerializer, RecipeSerializer,
                          ShortRecipeSerializer)


class RecipeViewSet(viewsets.ModelViewSet):
    
    queryset = Recipe.objects.all()
    pagination_class = RecipeViewSetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method in ("POST", "PATCH"):
            return RecipeCreateUpdateSerializer
        return RecipeSerializer

    def add_or_delete(self, request, model, pk=None):
        user = self.request.user
        if user.is_anonymous:
            return False
        recipe = get_object_or_404(Recipe, id=pk)
        check = model.objects.filter(
            user=user, recipe=recipe).exists()
        if self.request.method == "DELETE":
            if not check:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            favorite = get_object_or_404(
                model, user=user, recipe=recipe)
            favorite.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        if check:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        model.objects.create(user=user, recipe=recipe)
        serializer = ShortRecipeSerializer(
            recipe, context={"request": request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=("post", "delete"))
    def favorite(self, request, pk=None):
        return self.add_or_delete(request, FavoriteRecipe, pk)

    @action(detail=True, methods=("post", "delete"))
    def shopping_cart(self, request, pk=None):
        return self.add_or_delete(request, ShopingCard, pk)

    @action(detail=False, methods=("get",))
    def download_shopping_cart(self, request):
        shopping_cart = ShopingCard.objects.filter(user=self.request.user)
        recipes = shopping_cart.values_list("recipe__id", flat=True)
        buy_list = (
            IngredientsForRecipe.objects.filter(recipe__in=recipes)
            .values("ingredient")
            .annotate(total_amount=Sum("amount"))
        )
        return get_pdf_file(buy_list)


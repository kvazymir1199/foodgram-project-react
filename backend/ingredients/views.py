from django.shortcuts import render
from rest_framework import viewsets

# Create your views here.
from .serializers import IngredientSerializer, IngredientForRecipeSerializer
from .models import Ingredient, IngredientForRecipe


class IngredientView(viewsets.ModelViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()


class IngredientForRecipeView(viewsets.ModelViewSet):
    
    queryset = IngredientForRecipe.objects.all()
    serializer_class = IngredientForRecipeSerializer

        

    def get_queryset(self):
        print(super().get_queryset())
        return super().get_queryset()

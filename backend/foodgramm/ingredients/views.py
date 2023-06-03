from django.shortcuts import render
from rest_framework import viewsets

from .models import Ingredient
# Create your views here.
from .serializers import IngredientSerializer


class IngredientView(viewsets.ModelViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()

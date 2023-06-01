from django.shortcuts import render
from rest_framework import viewsets

# Create your views here.
from .serializers import IngredientSerializer
from .models import Ingredient


class IngredientView(viewsets.ModelViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()

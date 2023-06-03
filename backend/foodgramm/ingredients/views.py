from rest_framework import viewsets

from .models import Ingredient
from .serializers import IngredientSerializer


class IngredientView(viewsets.ModelViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()

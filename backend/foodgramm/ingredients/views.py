from rest_framework import viewsets,filters

from .models import Ingredient
from .serializers import IngredientSerializer


class IngredientView(viewsets.ModelViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)
    

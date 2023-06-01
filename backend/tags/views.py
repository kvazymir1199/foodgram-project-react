from django.shortcuts import render
from rest_framework import viewsets

# Create your views here.
from .models import Tag
from .serializers import TagSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def get_queryset(self):
        print(super().get_queryset())
        return super().get_queryset()
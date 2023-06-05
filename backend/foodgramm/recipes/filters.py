from distutils.util import strtobool

from django_filters.rest_framework import (FilterSet,
                                           ChoiceFilter,
                                           NumberFilter,
                                           ModelMultipleChoiceFilter)
from tags.models import Tag

from .models import (FavoriteRecipe,Recipe, ShopingCard)

CHOICES_LIST = (
    (0, "False"),
    (1, "True"),
)


class RecipeFilter(FilterSet):
    is_favorited = ChoiceFilter(
        choices=CHOICES_LIST, method="is_favorited_method"
    )
    is_in_shopping_cart = ChoiceFilter(
        choices=CHOICES_LIST, method="is_in_shopping_cart_method"
    )
    author = NumberFilter(
        field_name="author",
        lookup_expr="exact")
    tags = ModelMultipleChoiceFilter(
        field_name="tags__slug",
        to_field_name="slug",
        queryset=Tag.objects.all()
    )

    def is_favorited_method(self, queryset, name, value):
        if self.request.user.is_anonymous:
            return Recipe.objects.none()

        new_queryset = FavoriteRecipe.objects.filter(
            user=self.request.user
        ).values_list("recipe_id")
        if not strtobool(value):
            return queryset.difference(new_queryset)

        return queryset.filter(id__in=new_queryset)

    def is_in_shopping_cart_method(self, queryset, name, value):
        if self.request.user.is_anonymous:
            return Recipe.objects.none()
        new_queryset = ShopingCard.objects.filter(
            user=self.request.user).values_list(
            "recipe_id"
        )

        if not strtobool(value):
            return queryset.difference(new_queryset)

        return queryset.filter(id__in=new_queryset)

    class Meta:
        model = Recipe
        fields = ("author", "tags")

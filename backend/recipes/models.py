from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator

# Create your models here.

from ingredients.models import Ingredient
from tags.models import Tag
from django.core.validators import MinValueValidator

User = get_user_model()


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    ingredients = models.ManyToManyField(Ingredient, through="IngredientsForRecipe")
    name = models.CharField(max_length=100)
    tags = models.ManyToManyField(
        Tag, through="TagForRecipe", blank=True, related_name="recipes"
    )
    image = models.ImageField(upload_to="images/", blank=True)
    text = models.TextField(blank=True)
    cooking_time = models.SmallIntegerField(validators=[MinValueValidator(0)])

    def __str__(self) -> str:
        return self.name


class TagForRecipe(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)


class IngredientsForRecipe(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.PROTECT)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    amount = models.IntegerField(validators=[MinValueValidator(1)])


class FavoriteRecipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)


class ShopingCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзина"
        constraints = (
            models.UniqueConstraint(
                fields=("user", "recipe"), name="unique_shopping_card_recipe"
            ),
        )

    def __str__(self):
        return f"Рецепт {self.recipe} в списке покупок у {self.user}"

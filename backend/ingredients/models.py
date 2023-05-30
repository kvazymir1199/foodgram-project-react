from django.db import models
from django.core.validators import MinValueValidator


# Create your models here.
class Ingredient(models.Model):
    name = models.CharField(
        max_length=200, verbose_name="Ингредиент", help_text="Название ингредиента"
    )
    measurement_unit = models.CharField(
        max_length=10, verbose_name="Единица измерения", help_text="Единица измерения"
    )

    def __str__(self) -> str:
        return self.name


class IngredientForRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name="ingredient",
        verbose_name="Ингредиент в рецепте",
        help_text="Ингредиент в рецепте",
    )
    amount = models.IntegerField(
        validators=[
            MinValueValidator(1),
        ],
        help_text="Значение должно быть больше 1",
    )

    def __str__(self) -> str:
        return f"{self.ingredient.name} --> {self.amount}"

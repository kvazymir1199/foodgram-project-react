from django.db import models


# Create your models here.
class Ingredient(models.Model):
    name = models.CharField(
        max_length=200, verbose_name="Ингредиент",
        help_text="Название ингредиента"
    )
    measurement_unit = models.CharField(
        max_length=10,
        verbose_name="Единица измерения",
        help_text="Единица измерения"
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"

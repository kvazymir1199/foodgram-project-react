from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from ingredients.models import Ingredient
from tags.models import Tag

User = get_user_model()


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipes",
        verbose_name="Автор рецепта",
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through="IngredientsForRecipe",
        related_name="recipes",
        verbose_name="Игредиенты для рецепта",
        help_text="Введите игредиенты для рецепта",
    )
    name = models.CharField(
        max_length=100,
        verbose_name="Название рецепта",
        help_text="Введите название рецепта",
    )
    tags = models.ManyToManyField(
        Tag,
        through="TagForRecipe",
        related_name="recipes",
        verbose_name="Тег",
        help_text="Выберите тег",
    )
    image = models.ImageField(
        upload_to="images/",
        blank=True,
        verbose_name="Изображение",
        help_text="Добавьте изображение",
    )
    text = models.TextField(
        blank=True,
        verbose_name="Описание рецепта",
        help_text="Добавьте описание рецепта",
    )
    cooking_time = models.SmallIntegerField(
        validators=[MinValueValidator(0)],
        verbose_name="Время приготовления (в минутах)",
        help_text="Время приготовления (в минутах)",
    )

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"

    def __str__(self) -> str:
        return self.name


class TagForRecipe(models.Model):
    tag = models.ForeignKey(Tag,
                            on_delete=models.CASCADE,
                            related_name="tag_recipe")
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="recipe_tag"
    )

    class Meta:
        verbose_name = "Теги рецепта"
        verbose_name_plural = "Теги рецепта"
        constraints = (
            models.UniqueConstraint(
                fields=("tag", "recipe"), name="unique_tag_recipe"
            ),
        )

    def __str__(self) -> str:
        return f"В рецепте {self.recipe} указан тег:{self.tag}"


class IngredientsForRecipe(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.PROTECT)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name="amount_recipe")
    amount = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)])

    class Meta:
        verbose_name = "Ингредиенты рецепта"
        verbose_name_plural = "Ингредиенты рецепта"
        constraints = (
            models.UniqueConstraint(
                fields=("ingredient", "recipe"),
                name="unique_ingredient_recipe"
            ),
        )

    def __str__(self):
        return f"В рецепте {self.recipe} есть ингредиент {self.ingredient}"


class FavoriteRecipe(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="favorites",
        verbose_name="Пользователь",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="in_favorite",
        verbose_name="Рецепт",
    )

    class Meta:
        verbose_name = "Избранное"
        verbose_name_plural = "Избранное"

        constraints = (
            models.UniqueConstraint(
                fields=("user", "recipe"), name="unique_favorite_recipe"
            ),
        )


class ShopingCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="shopping")

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

# Generated by Django 2.2.28 on 2023-06-02 20:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_auto_20230602_1822'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='favoriterecipe',
            options={'verbose_name': 'Избранное', 'verbose_name_plural': 'Избранное'},
        ),
        migrations.AlterModelOptions(
            name='ingredientsforrecipe',
            options={'verbose_name': 'Ингредиенты рецепта', 'verbose_name_plural': 'Ингредиенты рецепта'},
        ),
        migrations.AlterModelOptions(
            name='recipe',
            options={'verbose_name': 'Рецепт', 'verbose_name_plural': 'Рецепты'},
        ),
        migrations.AlterModelOptions(
            name='tagforrecipe',
            options={'verbose_name': 'Теги рецепта', 'verbose_name_plural': 'Теги рецепта'},
        ),
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=models.ImageField(blank=True, help_text='Добавьте изображение', upload_to='images/', verbose_name='Изображение'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(help_text='Введите игредиенты для рецепта', related_name='recipes', through='recipes.IngredientsForRecipe', to='ingredients.Ingredient', verbose_name='Игредиенты для рецепта'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='name',
            field=models.CharField(help_text='Введите название рецепта', max_length=100, verbose_name='Название рецепта'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(help_text='Выберите тег', related_name='recipes', through='recipes.TagForRecipe', to='tags.Tag', verbose_name='Тег'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='text',
            field=models.TextField(blank=True, help_text='Добавьте описание рецепта', verbose_name='Описание рецепта'),
        ),
        migrations.AlterField(
            model_name='tagforrecipe',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipe_tag', to='recipes.Recipe'),
        ),
        migrations.AlterField(
            model_name='tagforrecipe',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tag_recipe', to='tags.Tag'),
        ),
    ]

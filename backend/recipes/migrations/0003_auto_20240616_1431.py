# Generated by Django 3.2 on 2024-06-16 07:31

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0002_auto_20240616_1350'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ingredient',
            options={'default_related_name': 'ingredient', 'verbose_name': 'Объект «Ингредиент»', 'verbose_name_plural': '«Ингредиенты»'},
        ),
        migrations.AlterModelOptions(
            name='recipe',
            options={'default_permissions': ('add', 'change', 'delete', 'view'), 'default_related_name': 'recipe', 'ordering': ('name', 'cooking_time'), 'verbose_name': 'объект «Рецепт»', 'verbose_name_plural': '«Рецепты»'},
        ),
        migrations.AlterField(
            model_name='recipe',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipe', to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(related_name='recipe', through='recipes.RecipeIngredient', to='recipes.Ingredient', verbose_name='Ингредиенты'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(related_name='recipe', through='recipes.RecipeTag', to='recipes.Tag', verbose_name='Теги'),
        ),
    ]

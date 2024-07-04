from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

from core import constants as const
from core.models import NameBaseModel
from recipes.validators import validate_cooking_time

User = get_user_model()


class Tag(NameBaseModel):
    name = models.CharField(
        max_length=const.INGREDIENT_NAME_MAX_LENGTH,
        verbose_name='Название',
    )
    slug = models.SlugField(
        verbose_name='Слаг',
        max_length=const.INGREDIENT_SLUG_MAX_LENGTH
    )

    class Meta:
        verbose_name = 'объект «Тег»'
        verbose_name_plural = '«Теги»'


class Ingredient(NameBaseModel):
    measurement_unit = models.CharField(
        max_length=const.MEASUREMENT_UNIT_MAX_LENGTH,
        verbose_name='Единица измерения веса'
    )

    class Meta:
        verbose_name = 'Объект «Ингредиент»'
        verbose_name_plural = '«Ингредиенты»'
        default_related_name = 'ingredient'


class Recipe(NameBaseModel):
    text = models.TextField('Описание')
    cooking_time = models.SmallIntegerField(
        validators=[validate_cooking_time],
        verbose_name='Время приготовления в минутах',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='recipes'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        verbose_name='Ингредиенты'
    )
    tags = models.ManyToManyField(
        Tag,
        through='RecipeTag',
        verbose_name='Теги'
    )
    image = models.ImageField(
        upload_to='recipes/images/',
        null=True,
        default=None,
        verbose_name='Фотография'
    )

    class Meta:
        default_related_name = 'recipe'
        verbose_name = 'объект «Рецепт»'
        verbose_name_plural = '«Рецепты»'
        ordering = ('name', 'cooking_time')
        default_permissions = (
            'add', 'change', 'delete', 'view'
        )


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        null=True,
        related_name='recipe_ingredient',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        null=True,
        related_name='recipe_ingredient'
    )
    amount = models.SmallIntegerField(
        verbose_name='Количество',
        validators=[
            MinValueValidator(
                const.AMOUNT_OF_INGREDIENT_MIN_VALUE,
                const.AMOUT_OF_INGREDIENT_MIN_VALUE_ERROR_MESSAGE
            )
        ],
        default=const.AMOUNT_OF_INGREDIENT_DEFAULT_VALUE
    )

    def __str__(self):
        return f'{self.amount}'


class RecipeTag(models.Model):
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.SET_NULL,
                               null=True,
                               related_name='recipestags')
    tag = models.ForeignKey(Tag,
                            on_delete=models.SET_NULL,
                            null=True,
                            related_name='recipestags')

    def __str__(self):
        return f'{self.recipe} {self.tag}'


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_recipe'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_recipe',
        null=True
    )


class FavoriteList(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite_recipe'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite_recipe'
    )


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик'
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор'
    )

    class Meta:
        verbose_name_plural = 'Объект «Подписка»'
        verbose_name_plural = '«Подписки»'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following'],
                name='unique_user_following'
            )
        ]

    def __str__(self):
        return self.following.username

from django.contrib.auth import get_user_model
from django.db import models

from core import constants as const

User = get_user_model()


class NameBaseModel(models.Model):
    name = models.CharField(max_length=const.NAME_MAX_LENGHT,
                            verbose_name='Название')

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return self.name


class UserRecipeBaseModel(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.CASCADE,
        null=True,
        verbose_name='Рецепт'
    )

    class Meta:
        abstract = True

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from core import constants as const


class FoodgramUser(AbstractUser):
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        'Имя пользователя',
        max_length=const.FOODGRAM_USERNAME_MAXLENGTH,
        unique=True,
        validators=[username_validator],
        error_messages={
            'unique': ('Пользователь с таким именем уже существует!'),
        },
    )
    email = models.EmailField(
        'Электронная почта',
        max_length=const.FOODGRAM_EMAIL_MAXLENGTH,
        unique=True,
        error_messages={
            'unique': (
                'Пользователь с такой почтой уже существует'
            )
        },
    )
    second_name = models.CharField(
        max_length=const.FOODGRAM_EMAIL_MAXLENGTH,
        null=True,
        verbose_name='Отчество'
    )
    role = models.CharField(
        'Роль пользователя',
        max_length=const.ROLE_MAX_LENGTH,
        choices=const.USER_ROLES_CHOICES,
        default=const.USER,
    )
    avatar = models.ImageField(
        upload_to='users/',
        null=True,
        default=None,
        blank=True
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('first_name', 'last_name',
                       'second_name', 'username')

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        ordering = ['username']

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == const.ADMIN or self.is_staff or self.is_superuser

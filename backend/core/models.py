from django.db import models

from core import constants as const


class NameBaseModel(models.Model):
    name = models.CharField(max_length=const.NAME_MAX_LENGHT,
                            verbose_name='Название')

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return self.name

from django.core.exceptions import ValidationError

from core import constants as const


def validate_cooking_time(value):
    if value < const.COOKING_TIME_MINIMAL_VALUE:
        raise ValidationError(message=const.COOKING_TIME_MINIMAL_VALUE)

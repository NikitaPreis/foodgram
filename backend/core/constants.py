NAME_MAX_LENGHT=256
USER_FOLLOW_THEMSELVES_ERROR_MESSAGE='Пользователь не может подписаться на себя'
SUBSCRIBE_DELETE_ERROR_MESSAGE='Невозможно удалить несуществующую подписку'
SUBSCRIBE_ERROR_MESSAGE='Подписка уже существует'
DUPLICATE_INGREDIENTS_ERROR_MESSAGE='Ингредиент указан больше 1-го раза'
DUPLICATE_TAGS_ERROR_MESSAGE='Тэг указан больше 1-го раза'
RECIPE_ALREADY_EXIST_IN_FAVORITE_LIST='Рецепт уже добавлен в избранное'
RECIPE_DOSNT_EXIST_IN_FAVORITE_LIST='Рецепт не был добавлен в избранное'
RECIPE_ALREADY_EXIST_IN_SHOPPING_CART='Рецепт уже добавлен в список покупок'
RECIPE_DOSNT_EXIST_IN_SHOPPING_CART='Рецепт не был добавлен в список покупок'
RECIPE_GET_LINK_ERROR_MESSAGE='Невозможно получить ссылку на рецепт'
AMOUNT_OF_INGREDIENT_MIN_VALUE=1
AMOUNT_OF_INGREDIENT_DEFAULT_VALUE=1
AMOUT_OF_INGREDIENT_MIN_VALUE_ERROR_MESSAGE=(f'Вес ингридиента не может '
                                             f'быть меньше '
                                             f'{AMOUNT_OF_INGREDIENT_MIN_VALUE}')
INGREDIENT_NAME_MAX_LENGTH=32
INGREDIENT_SLUG_MAX_LENGTH=32
PASSWORD_VALIDATION_ERROR_MESSAGE='Неверный пароль'
COOKING_TIME_MINIMAL_VALUE=1
COOKING_TIME_VALIDATION_ERROR_MASSAGE='Время приготовления не может быть меньше 1 минуты'
MEASUREMENT_UNIT_MAX_LENGTH=64
FOODGRAM_USERNAME_MAXLENGTH=150
FOODGRAM_EMAIL_MAXLENGTH=254
RECIPES_COUNT_DEFAULT_VALUE = 0
ADMIN='admin'
USER='user'
USER_ROLES_CHOICES=(
    (ADMIN, 'админ'),
    (USER, 'пользователь'),
)
ROLE_MAX_LENGTH = max(len(role[0]) for role in USER_ROLES_CHOICES)

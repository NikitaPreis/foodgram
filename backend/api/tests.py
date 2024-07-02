from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase

User = get_user_model()


class FoodgramAPITestCase(TestCase):
    USERNAME = 'TestUser'
    FIRST_NAME = 'Test'
    LAST_NAME = 'User'
    EMAIL = 'eudaimonia20@mail.ru'
    PASSWORD = 'TestPassword'

    @classmethod
    def setUpTestData(cls):
        cls.guest_client = Client()
        cls.user = User.objects.create(
            username=cls.USERNAME,
            password=cls.PASSWORD,
            email=cls.EMAIL,
            first_name=cls.FIRST_NAME,
            last_name=cls.LAST_NAME
        )
        cls.user_client = Client()
        cls.user_client.force_login(cls.user)

    def test_homepage_available(self):
        """Проверка доступности домашней страницы рецептов"""
        response = self.guest_client.get('/api/recipes/')
        self.assertEqual(response.status_code, HTTPStatus.OK)


# from http import HTTPStatus
# from django.contrib.auth import get_user_model
# from recipes.models import Ingredient, Recipe, Tag
# from django.test import Client, TestCase


# User = get_user_model()

# class FoodgramAPITestCase(TestCase):
#     USERNAME = 'TestUser'
#     FIRST_NAME = 'Test'
#     LAST_NAME = 'User'
#     EMAIL = 'eudaimonia20@mail.ru'
#     PASSWORD = 'TestPassword'

#     @classmethod
#     def setUpTestData(cls):
#         cls.guest_client = Client()
#         cls.user = User.objects.create(
#             username=cls.USERNAME,
#             password=cls.PASSWORD,
#             email=cls.EMAIL,
#             first_name=cls.FIRST_NAME,
#             last_name=cls.LAST_NAME
#         )
#         cls.user_client = Client()
#         cls.user_client.force_login(cls.user)
#         cls.login = cls.user_client.post(
#             '/api/auth/token/login/',
#             data={'email': cls.EMAIL,
#                   'password': cls.PASSWORD},
#              format='json', #follow=True
#         )
#         print(cls.login)
#         cls.token = cls.login['auth_token']

#         cls.ingredient = Ingredient.objects.create(
#             name='Капуста',
#             measurement_unit='кг'
#         )

#         cls.tag = Tag.objects.create(
#             name='Завтрак',
#             slug='breakfast'
#         )

#     def test_homepage_available(self):
#         """Проверка доступности домашней страницы рецептов"""
#         response = self.guest_client.get('/api/recipes/')
#         self.assertEqual(response.status_code, HTTPStatus.OK)

#     def test_recipe_create(self):
#         """Проверка создания рецепта авторизованным пользователем"""
#         data = {
#             'ingredients': {
#                 'id', 1,
#                 'amount', 10,
#             },
#             'tags': [
#                 1
#             ],
#             'image': '''data:image/png;base64,
# iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///
# 9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQ
# ImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==''',
#             'name': 'TestName',
#             'text': 'TextName',
#             'cooking_time': 1
#         }
#         response = self.user_client.post(
#             '/api/recipes/',
#             data=data,
#             format='json',
#             **{'HTTP_AUTHORIZATION': f'Token {self.token}'}
#             # **{'HTTP_AUTHORIZATION': f'Token {token}'}

#         )
#         self.assertEqual(response.status_code, HTTPStatus.CREATED)
#         self.assertTrue(Recipe.objects.filter(name='TestName').exists())

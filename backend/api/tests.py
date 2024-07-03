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

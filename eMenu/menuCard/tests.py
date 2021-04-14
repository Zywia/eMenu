# Create your tests here.
from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

from .models import User


class RegistrationTestCase(APITestCase):

    def setUp(self) -> None:
        self.password = "password"
        self.my_admin = User.objects.create_superuser('admin', 'admin@test.com', self.password)
        self.new_user = {"username": "user1",
                         "email": "user1@gamil.com",
                         "password": "password"}

    def test_registration_by_admin(self):
        self.assertTrue(self.my_admin.is_staff)
        self.client.login(username=self.my_admin.username, password=self.password)

        response = self.client.post("/api/register/", self.new_user)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        is_logged_in = self.client.login(**self.new_user)
        self.assertTrue(is_logged_in)

    def test_registration_no_login(self):
        response = self.client.post("/api/register/", self.new_user)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class GetCardsTestCase(APITestCase):
    def setUp(self) -> None:
        fake = Faker()

    def test_cards_get(self):
        response = self.client.get("/api/card/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetMealsTestCase(APITestCase):
    def setUp(self) -> None:
        self.password = "password"
        self.new_user = User.objects.create_user('user', 'user@test.com', self.password)

    def test_meals_get_logged_in(self):
        self.client.login(username=self.new_user.username, password=self.password)
        response = self.client.get("/api/meal/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_meals_get_not_logged(self):
        response = self.client.get("/api/meal/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

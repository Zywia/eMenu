# Create your tests here.
import random

from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

from .models import User, Card, Meal


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


class CardsTestsCase(APITestCase):
    def setUp(self) -> None:
        self.password = "password"
        self.new_user = User.objects.create_user('user', 'user@test.com', self.password)

        fake = Faker()
        description = fake.catch_phrase()
        price = random.randint(0, 30)
        time_to_prepare = fake.time()
        meal_object = Meal.objects.get_or_create(title=fake.company()[:20], description=description, price=price,
                                                 time_to_prepare=time_to_prepare)[0].id

        self.empty_card = Card.objects.get_or_create(title=fake.company()[:20], description=description)

        self.not_empty_card = Card.objects.create(title=fake.company()[:10], description=description)
        self.not_empty_card.meal.set([meal_object])
        self.not_empty_card.save()

    def test_cards_get(self):
        response = self.client.get("/api/card/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cards_get_public(self):
        response = self.client.get("/api/card/")
        self.assertEqual(len(response.data), 1)

    def test_cards_get_by_user(self):
        self.client.login(username=self.new_user.username, password=self.password)
        response = self.client.get("/api/card/")
        self.assertEqual(len(response.data), 2)

    def test_card_create(self):
        data = {"meal": [],
                "title": "string",
                "description": "string"}
        response = self.client.post("/api/card/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.login(username=self.new_user.username, password=self.password)
        response = self.client.post("/api/card/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(Card.objects.all()), 3)

    def test_card_update(self):
        data = {"meal": [],
                "title": "string1",
                "description": "string",
                "version": self.not_empty_card.version
                }
        self.client.login(username=self.new_user.username, password=self.password)
        response = self.client.put(f"/api/card/{self.not_empty_card.id}/", data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_card_delete(self):
        self.client.login(username=self.new_user.username, password=self.password)
        response = self.client.delete(f"/api/card/{self.not_empty_card.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(Card.objects.all()), 1)


class MealsTestsCase(APITestCase):
    def setUp(self) -> None:
        self.password = "password"
        self.new_user = User.objects.create_user('user', 'user@test.com', self.password)

        fake = Faker()
        description = fake.catch_phrase()
        price = random.randint(0, 30)
        time_to_prepare = fake.time()
        self.meal_object = Meal.objects.get_or_create(title=fake.company()[:20], description=description, price=price,
                                                      time_to_prepare=time_to_prepare)[0]

    def test_meals_get_logged_in(self):
        self.client.login(username=self.new_user.username, password=self.password)
        response = self.client.get("/api/meal/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_meals_get_not_logged(self):
        response = self.client.get("/api/meal/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_meals_create(self):
        data = {"title": "string",
                "description": "string",
                "price": "32",
                "time_to_prepare": "00:12:00"}

        self.client.login(username=self.new_user.username, password=self.password)
        response = self.client.post("/api/meal/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(Meal.objects.all()), 2)

    def test_meals_update(self):
        # response = self.client.get(f"/api/meal/{self.meal_object}/")
        data = {"title": "string",
                "description": "string",
                "price": "32",
                "time_to_prepare": "00:12:00",
                "version": self.meal_object.version}

        self.client.login(username=self.new_user.username, password=self.password)
        response = self.client.put(f"/api/meal/{self.meal_object.id}/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_meals_delete(self):
        self.client.login(username=self.new_user.username, password=self.password)
        response = self.client.delete(f"/api/meal/{self.meal_object.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(Meal.objects.all()), 0)

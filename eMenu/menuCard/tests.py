# Create your tests here.

from rest_framework import status
from rest_framework.test import APITestCase


class RegistrationTestCase(APITestCase):

    def test_registration(self):
        data = {"username": "user1",
                "email": "user1@gamil.com",
                "password": "password"}
        response = self.client.post("/api/register/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class GetCardsTestCase(APITestCase):

    def test_cards_get(self):
        response = self.client.get("/api/card/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

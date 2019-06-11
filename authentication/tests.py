from django.test import TestCase

from rest_framework.test import APITestCase
from rest_framework.test import APIClient

from rest_framework.test import APIRequestFactory

from rest_framework import status

from django.contrib.auth import get_user_model
from django.urls import reverse

# Create your tests here.


class UserModelTestCase(TestCase):
    def setUp(self):
        """Define the test client and other test variables."""
        self.User = get_user_model()
        self.user_1 = self.User.objects.create_user(
            first_name='user',
            last_name='user1',
            email='user@foo.com',
            password='pass'
        )
        self.user_2 = self.User.objects.create_user(
            first_name="Kent",
            last_name="Philip",
            password="Phrase908",
            email="kent@gmail.com",
        )

    def test_user_creation_is_successful(self):
        """Test the user created exist in the user model."""
        user_1 = self.User.objects.get(pk=self.user_1.id)
        user_2 = self.User.objects.get(pk=self.user_2.id)
        user_count = self.User.objects.count()

        self.assertEqual(user_1.first_name, "user")
        self.assertEqual(user_2.first_name, "Kent")
        self.assertEqual(user_count, 2)

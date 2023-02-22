"""
Test for user API
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**params):
    """Create and return new user"""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Public featurese of user API tests"""
    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Test creating user is successfull"""
        payload = {
            'email': 'test@example.com',
            'password': 'abv123123',
            'name': 'Anemd'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_with_email_exists_error(self):
        """Test error returned if user with email exists"""
        payload = {
            'email': 'test@example.com',
            'password': 'abv123',
            'name': 'Anemd'
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """Test error returned if password less than 5 chars"""
        payload = {
            'email': 'test@example.com',
            'password': 'ab3',
            'name': 'Anemd'
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Generates token for valid credentials"""
        user_details = {
            'name': 'Anemd',
            'email': 'test@example.com',
            'password': 'ab3Fik346SK',
        }
        create_user(**user_details)

        payload = {
            'email': user_details['email'],
            'password': user_details['password'],
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_bad_credentials(self):
        """Generates error for invalid credentials"""
        user_details = {
            'email': 'test@example.com',
            'password': 'ab3Fik346SK',
            'name': 'Anemd',
        }
        create_user(**user_details)

        payload = {
            'email': user_details['email'],
            'password': 'badpass',
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password(self):
        """Generates error for blank password"""

        payload = {
            'email': 'est@example.com',
            'password': '',
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

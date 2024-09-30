"""
Tests for user API
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')

User = get_user_model()


def create_user(**kwargs):
    return User.objects.create_user(**kwargs)


class PublicUserAPITests(TestCase):
    """Test the public features of the user API"""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Test creating a user successfull"""
        payload = {
            'email': 'testuser1@example.com',
            'name': 'test_user1',
            'password': 'test@1234',
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_with_email_exists_error(self):
        """Test error if user email already exists"""

        payload = {
            'email': 'testuser2@example.com',
            'name': 'test_user2',
            'password': 'test@1234',
        }

        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        # if new user is registered with existing email, throws error
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_not_secure_error(self):
        """Test an error if user password is not secure"""
        payload = {
            'email': 'testuser3@example.com',
            'name': 'test_user3',
            'password': 'test',
        }

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        # to check if above user is not created in DB
        user_exists = User.objects.filter(email=payload['email']).exists()
        self.assertFalse(user_exists)

    def test_create_token_user_success(self):
        """Test token is created for valid user credentials"""
        user_details = {
            'email': 'testuser4@example.com',
            'name': 'test_user4',
            'password': 'test@1234',
        }
        create_user(**user_details)

        payload = {
            'email': user_details['email'],
            'password': user_details['password'],
        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('token', res.data)

    def test_create_token_without_credentials(self):
        """Test token should not be created for GET request"""
        res = self.client.get(TOKEN_URL)
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_create_token_invalid_credentials(self):
        """Test token should not be created for invalid credentials"""
        user_details = {
            'email': 'testuser5@example.com',
            'name': 'test_user5',
            'password': 'test@1234',
        }
        create_user(**user_details)

        payload = {
            'email': 'testuser555@example.com',
            'password': user_details['password'],
        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

    def test_create_token_blank_password(self):
        """Test token should not be created for blank password"""
        payload = {
            'email': 'testuser5@example.com',
            'password': '',
        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

    def test_user_retrieve_unauthorized(self):
        """Test authentication is required for user profile access"""
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserAPITests(TestCase):
    """Test API requests that requies authentication"""

    def setUp(self):
        self.user = create_user(email='test6@example.com',
                                name='test_user5', password='test@1234')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_user_details_success(self):
        """Test user profile retrieved for authenticated user"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'name': self.user.name,
            'email': self.user.email,
        })

    def test_retrieve_post_user_not_allowed(self):
        """Test POST is not allowed for user profile"""
        payload = {
            'email': 'testuser5@example.com',
            'password': '',
        }
        res = self.client.post(ME_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating user for authenticated user"""
        payload = {
            'email': 'testuser5@example.com',
            'password': 'test@1234',
            'name': 'test_user5',
        }
        res = self.client.patch(ME_URL, payload)
        self.user.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.email, payload['email'])
        self.assertTrue(self.user.check_password(payload['password']))

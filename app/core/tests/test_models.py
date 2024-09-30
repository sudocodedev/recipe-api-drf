"""
Test for models
"""

from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    """Test models."""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful"""
        email = "test@example.com"
        password = "test@1234"

        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalize(self):
        """Test a new user mail is normalized"""
        sample_emails = [
            ['test1@example.com', 'test1@example.com'],
            ['Test2@EXAMPLE.com', 'Test2@example.com'],
            ['TesT3@Example.COM', 'TesT3@example.com'],
            ['TEST4@EXAMPLE.COM', 'TEST4@example.com'],
        ]

        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'test@1234')
            self.assertEqual(user.email, expected)

    def test_create_user_without_email_error(self):
        """Test creating a user without email"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test@1234')

    def test_create_superuser(self):
        """Test creating a superuser"""
        user = get_user_model().objects.create_superuser(
            email='test5@example.com',
            password='test@1234',
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

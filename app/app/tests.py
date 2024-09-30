"""
Test for the django admin modifications
"""

from django.test import TestCase, Client  # allows to make HTTP requests
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTest(TestCase):
    """Tests for django admin"""

    def setUp(self):
        """create user and client"""
        self.client = Client()

        # superuser
        self.admin_user = get_user_model().objects.create_superuser(
            email='user1@example.com',
            password='test@1234',
        )
        self.client.force_login(self.admin_user)

        # regular user
        self.user = get_user_model().objects.create_user(
            email='user12@example.com',
            password='test@1234',
            name='Test User',
        )

    def test_users_list(self):
        """Tests that users are listed on the admin page"""
        url = reverse("admin:core_user_changelist")
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_edit_user_page(self):
        """Test the edit user page works"""
        url = reverse("admin:core_user_change", args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test the create user page works"""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

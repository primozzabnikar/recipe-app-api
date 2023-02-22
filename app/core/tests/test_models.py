"""
test for models
"""

from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTest(TestCase):
    """Test models"""

    def test_create_user_with_email_successful(self):
        """Test creatinf a user with an email is successful"""
        email = 'test@example.com'
        password = 'testpas123R'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_ner_user_email_normalized(self):
        """Test email is normalized for new users"""
        sample_emails = [
            ['test1@example.COM', 'test1@example.com'],
            ['Test2@Example.COM', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['TEST4@EXAMPLE.com', 'TEST4@example.com'],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'Sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_emai_raises_error(self):
        """Test that creating a user with blank email raises a ValueError """
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')

    def test_create_supoeruser(self):
        """Test creating super user"""
        user = get_user_model().objects.create_superuser(
            'test@Example.com',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

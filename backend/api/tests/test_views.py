from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from unittest.mock import patch
from django.conf import settings

User = get_user_model()

class UserTestCase(TestCase):
    def helper_create_user(self):
        user = User.objects.create(
            name = "Chuck Onwu",
            email = "chuck@example.com",
            password = make_password('Supreme1')
        )
        return user


@patch('api.views.users_views.send_mail')
class RegisterUserAPITests(UserTestCase):
    def test_user_can_be_registered(self, mock_send_mail):
        self.assertRaises(User.DoesNotExist, User.objects.get, email="chuck@example.com" )
        response = self.client.post('/api/users/register/', data={'name': 'Chuck Onwu', 'email': 'chuck@example.com', 'password': 'Supreme1'})
        self.assertEqual(response.status_code, 200)
        user = User.objects.get(email='chuck@example.com')
        self.assertIsNotNone(user)
    
    def test_registered_user_has_correct_settings(self, mock_send_mail):
        self.assertRaises(User.DoesNotExist, User.objects.get, email='chuck@example.com' )
        response = self.client.post('/api/users/register/', data={'name': 'Chuck Onwu', 'email': 'chuck@example.com', 'password': 'Supreme1'})
        user = User.objects.get(email='chuck@example.com')
        self.assertEqual(user.name, 'Chuck Onwu')
        self.assertEqual(user.email, 'chuck@example.com')
        self.assertFalse(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.sent_verification_email)
        self.assertFalse(user.verified_email)

    def test_missing_name_returns_bad_request(self, mock_send_mail):
        response = self.client.post('/api/users/register/', data={'email': 'chuck@example.com', 'password': 'Supreme1'})
        self.assertEqual(response.status_code, 400)
    
    def test_missing_email_returns_bad_request(self, mock_send_mail):
        response = self.client.post('/api/users/register/', data={'name': 'Chuck Onwu', 'password': 'Supreme1'})
        self.assertEqual(response.status_code, 400)
    
    def test_missing_password_returns_bad_request(self, mock_send_mail):
        response = self.client.post('/api/users/register/', data={'email': 'chuck@example.com', 'name': 'Chuck Onwu'})
        self.assertEqual(response.status_code, 400)

    def test_existing_user_returns_error_message(self, mock_send_mail):
        self.helper_create_user()
        response = self.client.post('/api/users/register/', data={'email': 'chuck@example.com', 'name': 'Chuck Onwu', 'password': 'Supreme1'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['message'], "User already exists")

    def test_registered_user_gets_verification_email(self, mock_send_mail):
        self.assertEqual(User.DoesNotExist, User.objects.get, email='chuck1@example.com')
        response = self.client.post('/api/users/register/', data={'email': 'chuck1@example.com', 'name': 'Chuck Onwu', 'password': 'Supreme1'})
        user = User.objects.get(email='chuck@example.com')
        self.assertTrue(user.sent_verification_email)
        self.assertEqual(mock_send_mail.called, True)
        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
        self.assertEqual(subject, f"Verify tour user account for {settings.WEB_SITE_NAME}")
        self.assertEqual(body, f"To verify yoit acount for {settings.WEB_SITE_NEWS}")
        self.assertEqual(from_email, settings.SENDER_EMAIL)
        self.assertEqual(to_list, ['chuck@example.com'])
        self.assertIn("html_message", kwargs)
        for key, value in kwargs.items:
            if key == "html_message":
                self.assertEqual(value, f'Please <a href="{settings.VERIFICATION_URL}">click this link</a> to verify your user account for {settings.WEB_SITE_NAME}.')
from django.test import TestCase # type: ignore
from django.contrib.auth import get_user_model # type: ignore
from django.contrib.auth.models import User # type: ignore
from django.contrib.auth.hashers import make_password # type: ignore

User = get_user_model()

class UserTestCase(TestCase):
    def helper_create_user(self):
        user = User.objects.create(
            name = "Chuck Onwu",
            email = "chuck@example.com",
            password = make_password('Supreme1')
        )
        return user
    
class RegisterUserAPITests(UserTestCase):
    def test_user_can_be_registered(self):
        self.assertRaises(User.DoesNotExist, User.objects.get, email="chuck@example.com" )
        response = self.client.post('/api/users/register/', data={'name': 'Chuck Onwu', 'email': 'chuck@example.com', 'password': 'Supreme1'})
        self.assertEqual(response.status_code, 200)
        user = User.objects.get(email='chuck@example.com')
        self.assertIsNotNone(user)
    
    def test_registered_user_has_correct_settings(self):
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

    def test_missing_name_returns_bad_request(self):
        response = self.client.post('/api/users/register/', data={'email': 'chuck@example.com', 'password': 'Supreme1'})
        self.assertEqual(response.status_code, 400)
    
    def test_missing_email_returns_bad_request(self):
        response = self.client.post('/api/users/register/', data={'name': 'Chuck Onwu', 'password': 'Supreme1'})
        self.assertEqual(response.status_code, 400)
    
    def test_missing_password_returns_bad_request(self):
        response = self.client.post('/api/users/register/', data={'email': 'chuck@example.com', 'name': 'Chuck Onwu'})
        self.assertEqual(response.status_code, 400)

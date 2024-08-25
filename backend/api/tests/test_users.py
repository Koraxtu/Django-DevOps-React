from django.contrib.auth import get_user_model # type: ignore
from django.test import TestCase # type: ignore

class UsersManagersTests(TestCase): # type: ignore

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(email='chuck@example.com', password='foo', name="Chuck Onwu")
        self.assertEqual(user.email, 'chuck@example.com')
        self.assertEqual(user.name, 'Chuck Onwu')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        try:
            # username is None for th AbtractUser option
            # username does not exist for the AstractBaseUser option
            self.assertIsNone(user.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email="")
        with self.assertRaises(ValueError):
            User.objects.create_user(email="", password="foo")
        
    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(email='super@example.com', password='foo', name="Chuck Onwu")
        self.assertEqual(admin_user.email, 'super@example.com')
        self.assertEqual(admin_user.name, 'Chuck Onwu')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        try:
            # username is None for th AbtractUser option
            # username does not exist for the AstractBaseUser option
            self.assertIsNone(admin_user.username)
        except AttributeError:
            pass
        with self.assertRaises(ValueError):
            User.objects.create_superuser(email="", password="foo", is_superuser=False)
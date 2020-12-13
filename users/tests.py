from django.contrib.auth import get_user_model
from django.test import TestCase
from django.contrib.auth import authenticate
from .models import User

class UserTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='test',
                                                         password='12test12',
                                                         email='test@example.com')
        self.user.save()

    def tearDown(self):
        self.user.delete()

    def test_correct(self):
        user = authenticate(username='test', password='12test12')
        self.assertTrue(user is not None and user.is_authenticated)

    def test_wrong_username(self):
        with self.assertRaises(AttributeError):
            authenticate(username='wrong', password='12test12')

    def test_wrong_password(self):
        with self.assertRaises(AttributeError):
            authenticate(username='test', password='wrong')

    def test_pages_without_login(self):
        response = self.client.get('/users/login/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/users/profile/')
        self.assertEqual(response.status_code, 302)
        response = self.client.get('/users/password/')
        self.assertEqual(response.status_code, 302)
        response = self.client.get('/users/logout/')
        self.assertEqual(response.status_code, 200)


    def test_pages_with_login(self):
        response = self.client.get('/users/login/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/users/login/', username='test', password='12test12')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/users/profile/', username='test', password='12test12', follow=True)
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/users/password/', username='test', password='12test12', follow=True)
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/users/logout/', username='test', password='12test12', follow=True)
        self.assertEqual(response.status_code, 200)

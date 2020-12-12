from django.test import TestCase
from .models import User

class UserTestCase(TestCase):
    def setUp(self):
        User.objects.create(username="user1", password="password1")

    def test1(self):
        UserName = User.objects.get(username="user1")
        self.assertEqual(UserName.username, "user1")

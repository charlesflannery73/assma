from django.core.exceptions import ValidationError
from django.test import TestCase
from .models import Org, Asset
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.contrib.auth.models import User, Permission, Group
from django.test import Client

class OrgTestCase(TestCase):
    def setUp(self):
        Org.objects.create(id=1, name="test_org", sector="Education", comment="test org comment")
        Asset.objects.create(name="1.2.3.4", org=Org(1), type="ipv4", comment="test asset comment")
        Asset.objects.create(name="example.com", org=Org(1), type="domain", comment="test asset comment")


    def test_retrieving_inserted_org_data(self):
        OrgName = Org.objects.get(name="test_org")
        self.assertEqual(OrgName.name, "test_org")
        self.assertEqual(OrgName.tier, 5)
        self.assertEqual(OrgName.level, "National")
        self.assertEqual(OrgName.sector, "Education")
        self.assertEqual(OrgName.comment, "test org comment")

    def test_retrieving_inserted_asset_data(self):
        AssetName = Asset.objects.get(name="1.2.3.4")
        self.assertEqual(AssetName.name, "1.2.3.4")
        self.assertEqual(AssetName.type, "ipv4")
        self.assertEqual(AssetName.org, Org(1))
        self.assertEqual(AssetName.comment, "test asset comment")

    def test_nslookup(self):
        AssetName = Asset.objects.get(name="example.com")
        self.assertRegex(AssetName.comment, '__ips: [0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}')

    def test_duplicate_org(self):
        with self.assertRaises(Exception):
            Org.objects.create(name="test_org", sector="Education")

    def test_duplicate_asset(self):
        with self.assertRaises(Exception):
            Asset.objects.create(name="1.2.3.4", org=Org(1), type="ipv4")

    def test_invalid_ipv4(self):
        with self.assertRaises(ValidationError):
            Asset.objects.create(name="1.2.3", org=Org(1), type="ipv4")

    def test_invalid_ipv6(self):
        with self.assertRaises(ValidationError):
            Asset.objects.create(name="1.2.3", org=Org(1), type="ipv6")

    def test_invalid_domain(self):
        with self.assertRaises(ValidationError):
            Asset.objects.create(name="123", org=Org(1), type="domain")

    def test_invalid_cidr4(self):
        with self.assertRaises(ValidationError):
            Asset.objects.create(name="1.1.1.0", org=Org(1), type="cidr4")

    def test_invalid_cidr6(self):
        with self.assertRaises(ValidationError):
            Asset.objects.create(name="1.1.1.1", org=Org(1), type="cidr6")

    def test_invalid_range4(self):
        with self.assertRaises(ValidationError):
            Asset.objects.create(name="1.1.1.1", org=Org(1), type="range4")

    def test_invalid_range6(self):
        with self.assertRaises(ValidationError):
            Asset.objects.create(name="1.1.1.1", org=Org(1), type="range6")

    def test_invalid_netmask4(self):
        with self.assertRaises(ValidationError):
            Asset.objects.create(name="1.1.1.0/24", org=Org(1), type="netmask4")

    def test_pages_without_login(self):
        response = self.client.get('/', follow=True)
        self.assertRedirects(response, '/users/login/?next=/', status_code=302, target_status_code=200)
        response = self.client.get('/about', follow=True)
        self.assertRedirects(response, '/users/login/?next=/about/', status_code=301, target_status_code=200)
        response = self.client.get('/admin', follow=True)
        self.assertRedirects(response, '/admin/login/?next=/admin/', status_code=301, target_status_code=200)
        response = self.client.get('/org', follow=True)
        self.assertRedirects(response, '/users/login/?next=/org/', status_code=301, target_status_code=200)
        response = self.client.get('/org/search/', follow=True)
        self.assertRedirects(response, '/users/login/?next=/org/search/', status_code=302, target_status_code=200)
        response = self.client.get('/org/new/', follow=True)
        self.assertRedirects(response, '/users/login/?next=/org/new/', status_code=302, target_status_code=200)
        response = self.client.get('/asset', follow=True)
        self.assertRedirects(response, '/users/login/?next=/asset/', status_code=301, target_status_code=200)
        response = self.client.get('/asset/search/', follow=True)
        self.assertRedirects(response, '/users/login/?next=/asset/search/', status_code=302, target_status_code=200)
        response = self.client.get('/asset/new/', follow=True)
        self.assertRedirects(response, '/users/login/?next=/asset/new/', status_code=302, target_status_code=200)


    def test_pages_with_read_only_login(self):
        user = get_user_model().objects.create_user(username='test', password='12test12', email='test@example.com')
        self.client.force_login(user=user)

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/about/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/org/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/org/search/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/org/new/')
        self.assertEqual(response.status_code, 403)
        response = self.client.get('/org/1/update/')
        self.assertEqual(response.status_code, 403)
        response = self.client.get('/org/1/delete/')
        self.assertEqual(response.status_code, 403)

        response = self.client.get('/asset/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/asset/search/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/asset/new/')
        self.assertEqual(response.status_code, 403)
        response = self.client.get('/asset/1/update/')
        self.assertEqual(response.status_code, 403)
        response = self.client.get('/asset/1/delete/')
        self.assertEqual(response.status_code, 403)


    def test_pages_with_assma_manager_perms(self):
        user = get_user_model().objects.create_user(username='manager', password='12test12', email='test@example.com')
        user.user_permissions.add(29, 30, 31, 33, 34, 35)
        user.save()
        self.client.force_login(user=user)

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/about/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/org/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/org/search/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/org/new/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/org/1/update/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/org/1/delete/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/asset/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/asset/search/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/asset/new/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/asset/1/update/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/asset/1/delete/')
        self.assertEqual(response.status_code, 200)



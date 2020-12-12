from django.core.exceptions import ValidationError
from django.test import TestCase
from .models import Org, Asset

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

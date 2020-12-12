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
        try:
            Org.objects.create(name="test_org", sector="Education")
        except:
            self.assertEqual("1", "1")
        else:
            raise Exception("test_org is duplicate and should have raised an exception but didn't")

    def test_duplicate_asset(self):
        try:
            Asset.objects.create(name="1.2.3.4", org=Org(1), type="ipv4")
        except:
            self.assertEqual("1", "1")
        else:
            raise Exception("1.2.3.4 is duplicate and should have raised an exception but didn't")

    def test_invalid_ipv4(self):
        try:
            Asset.objects.create(name="1.2.3", org=Org(1), type="ipv4")
        except:
            self.assertEqual("1", "1")
        else:
            raise Exception("invalid ipv4 1.2.3 should have raised an exception but didn't")

    def test_invalid_ipv6(self):
        try:
            Asset.objects.create(name="1.2.3", org=Org(1), type="ipv6")
        except:
            self.assertEqual("1", "1")
        else:
            raise Exception("invalid ipv6 1.2.3 should have raised an exception but didn't")

    def test_invalid_domain(self):
        try:
            Asset.objects.create(name="123", org=Org(1), type="domain")
        except:
            self.assertEqual("1", "1")
        else:
            raise Exception("invalid domain 123 should have raised an exception but didn't")

    def test_invalid_cidr4(self):
        try:
            Asset.objects.create(name="1.1.1.0", org=Org(1), type="cidr4")
        except:
            self.assertEqual("1", "1")
        else:
            raise Exception("invalid cidr4 1.1.1.0 should have raised an exception but didn't")

    def test_invalid_cidr6(self):
        try:
            Asset.objects.create(name="1.1.1.1", org=Org(1), type="cidr6")
        except:
            self.assertEqual("1", "1")
        else:
            raise Exception("invalid cidr6 1.1.1.1 should have raised an exception but didn't")

    def test_invalid_range4(self):
        try:
            Asset.objects.create(name="1.1.1.1", org=Org(1), type="range4")
        except:
            self.assertEqual("1", "1")
        else:
            raise Exception("invalid range4 1.1.1.1 should have raised an exception but didn't")

    def test_invalid_range6(self):
        try:
            Asset.objects.create(name="1.1.1.1", org=Org(1), type="range6")
        except:
            self.assertEqual("1", "1")
        else:
            raise Exception("invalid range6 1.1.1.1 should have raised an exception but didn't")

    def test_invalid_netmask4(self):
        try:
            Asset.objects.create(name="1.1.1.0/24", org=Org(1), type="netmask4")
        except:
            self.assertEqual("1", "1")
        else:
            raise Exception("invalid netmask4 1.1.1.0/24 should have raised an exception but didn't")

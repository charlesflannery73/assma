from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.db import models
import ipaddress
import re
import validators

class Sector(models.Model):
    sector = models.CharField(max_length=255, null=False)

    def __str__(self):
        return self.sector


class Level(models.Model):
    level = models.CharField(max_length=255, null=False)

    def __str__(self):
        return self.level


class Org(models.Model):

    name = models.CharField(max_length=255, null=False, unique=True)
    sector = models.ForeignKey(Sector, on_delete=models.PROTECT)
    level = models.ForeignKey(Level, on_delete=models.PROTECT)
    tier = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], default=5)
    comment = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse('org-detail', kwargs={'pk': self.pk})


class AssetType(models.Model):
    type = models.CharField(max_length=255, null=False)

    def __str__(self):
        return self.type


# noinspection PyTypeChecker
class Asset(models.Model):
    name = models.CharField(max_length=255, null=False, unique=True)
    org = models.ForeignKey(Org, on_delete=models.PROTECT)
    type = models.ForeignKey(AssetType, on_delete=models.PROTECT)
    comment = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.name

    def save(self, **kwargs):
        self.clean()
        return super(Asset, self).save(**kwargs)

    def clean(self):
        super(Asset, self).clean()

        if str(self.type) == "ipv4":
            try:
                ipaddress.IPv4Address(str(self.name))
            except ValueError:
                raise ValidationError('\"' + self.name + '\" is not a valid ipv4 address')

        if str(self.type) == "ipv6":
            try:
                ipaddress.IPv6Address(str(self.name))
            except ValueError:
                raise ValidationError('\"' + self.name + '\" is not a valid ipv6 address')

        if str(self.type) == "cidr4":
            try:
                ipaddress.IPv4Network(str(self.name))
            except ValueError:
                raise ValidationError('\"' + self.name + '\" is not a valid ipv4 cidr address')

        if str(self.type) == "cidr6":
            try:
                ipaddress.IPv6Network(str(self.name))
            except ValueError:
                raise ValidationError('\"' + self.name + '\" is not a valid ipv6 cidr address')

        if str(self.type) == "range4":
            match = re.search('[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}-[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}', self.name,  )
            if match:
                pair = self.name.split("-")
                test = ipaddress.IPv4Address(pair[1]) > ipaddress.IPv4Address(pair[0])
                if test == False:
                    raise ValidationError('\"' + pair[1] + '\" is not higher than \"' + pair[0] + '\" try again!')

                for ip4 in pair:
                    try:
                        ipaddress.IPv4Address(str(ip4))
                    except ValueError:
                        raise ValidationError('\"' + ip4 + '\" is not a valid ipv4 address')
            else:
                raise ValidationError('\"' + self.name + '\" is not a valid range4 address, please use a hyphen as a separator eg 1.2.3.4-1.2.3.8')

        if str(self.type) == "range6":
            match = re.search('[0-9a-f:]+-[0-9a-f:]+', self.name, re.I)
            if match:
                pair = self.name.split("-")
                test = ipaddress.IPv6Address(pair[1]) > ipaddress.IPv6Address(pair[0])
                if test == False:
                    raise ValidationError('\"' + pair[1] + '\" is not higher than \"' + pair[0] + '\" try again!')
                for ip6 in pair:
                    try:
                        ipaddress.IPv6Address(str(ip6))
                    except ValueError:
                        raise ValidationError('\"' + ip6 + '\" is not a valid ipv6 address')
            else:
                raise ValidationError('\"' + self.name + '\" is not a valid range6 address, please use a hyphen as a separator eg 2001:db8::-2001:db8:0000:0000:0000:0000:0000:00ff')

        if str(self.type) == "mask4":
            match = re.search('/', self.name,  )
            if match:
                try:
                    ipaddress.IPv4Network(str(self.name))
                except ValueError:
                    raise ValidationError('\"' + self.name + '\" is not a valid ipv4 netmask, please use forward slash as separator eg 192.168.10.0/255.255.255.0')
            else:
                raise ValidationError('\"' + self.name + '\" is not a valid ipv4 netmask, please use forward slash as separator eg 192.168.10.0/255.255.255.0')

        if str(self.type) == "domain":
            test = validators.domain(self.name)
            if test != True:
                raise ValidationError('\"' + self.name + '\" is not a valid domain name')


    # def get_absolute_url(self):
    #     return reverse('asset-detail', kwargs={'pk': self.pk})


from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
import ipaddress
import re
import validators
import socket

class Org(models.Model):

    LEVEL_FEDERAL = 'Federal'
    LEVEL_STATE = 'State'
    LEVEL = [
        (LEVEL_FEDERAL, 'Federal / National level'),
        (LEVEL_STATE, 'State level'),
    ]

    SECTOR_ENERGY = 'Energy, Utilities, Agriculture'
    SECTOR_SECURITY = 'Safety and Security'
    SECTOR_DEFENSE = 'Defense and Intelligence'
    SECTOR_ICT = 'ICT'
    SECTOR_TRANSPORTATION = 'Transportation'
    SECTOR_ADMIN = 'Government Administration'
    SECTOR_EDUCATION = 'Education'
    SECTOR_MEDIA = 'Media, Entertainment'
    SECTOR_FINANCE = 'Finance and Economy'
    SECTOR_SPECIAL = 'Special'
    SECTOR_HEALTH = 'Healthcare'
    SECTOR_MANUFACTURING = 'Manufacturing, Construction'
    SECTOR = [
        (SECTOR_ENERGY, 'Energy, Utilities, Agriculture'),
        (SECTOR_SECURITY, 'Safety and Security'),
        (SECTOR_DEFENSE, 'Defense and Intelligence'),
        (SECTOR_ICT, 'ICT'),
        (SECTOR_TRANSPORTATION, 'Transportation'),
        (SECTOR_ADMIN, 'Government Administration'),
        (SECTOR_EDUCATION, 'Education'),
        (SECTOR_MEDIA, 'Media, Entertainment'),
        (SECTOR_FINANCE, 'Finance and Economy'),
        (SECTOR_SPECIAL, 'Special'),
        (SECTOR_HEALTH, 'Healthcare'),
        (SECTOR_MANUFACTURING, 'Manufacturing, Construction'),
    ]

    name = models.CharField(max_length=255, null=False, unique=True)
    level = models.CharField(max_length=255, choices=LEVEL, default=LEVEL_FEDERAL)
    sector = models.CharField(max_length=255, choices=SECTOR, default=SECTOR_ADMIN)
    tier = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], default=5)
    comment = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Asset(models.Model):
    TYPE_DOMAIN = 'domain'
    TYPE_IPV4 = 'ipv4'
    TYPE_RANGE4 = 'range4'
    TYPE_NETMASK4 = 'netmask4'
    TYPE_CIDR4 = 'cidr4'
    TYPE_IPV6 = 'ipv6'
    TYPE_RANGE6 = 'range6'
    TYPE_CIDR6 = 'cidr6'
    TYPE = [
        (TYPE_DOMAIN, 'domain'),
        (TYPE_IPV4, 'ipv4'),
        (TYPE_RANGE4, 'range4'),
        (TYPE_NETMASK4, 'netmask4'),
        (TYPE_CIDR4, 'cidr4'),
        (TYPE_IPV6, 'ipv6'),
        (TYPE_RANGE6, 'range6'),
        (TYPE_CIDR6, 'cidr6'),
    ]

    name = models.CharField(max_length=255, null=False, unique=True)
    org = models.ForeignKey(Org, on_delete=models.PROTECT)
    type = models.CharField(max_length=255, choices=TYPE)
    start_ip = models.UUIDField(blank=True)
    end_ip = models.UUIDField(blank=True)
    comment = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

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
            except:
                raise ValidationError('\"' + self.name + '\" is not a valid ipv4 address')
            self.start_ip = int(ipaddress.IPv4Address(self.name))
            self.end_ip = int(ipaddress.IPv4Address(self.name))

        if str(self.type) == "ipv6":
            try:
                ipaddress.IPv6Address(str(self.name))
            except:
                raise ValidationError('\"' + self.name + '\" is not a valid ipv6 address')
            self.start_ip = int(ipaddress.IPv6Address(self.name))
            self.end_ip = int(ipaddress.IPv6Address(self.name))

        if str(self.type) == "cidr4":
            match = re.search('/', self.name,  )
            if match:
                try:
                    ipaddress.IPv4Network(str(self.name))
                except:
                    raise ValidationError('\"' + self.name + '\" is not a valid ipv4 network address')
                self.start_ip = int(ipaddress.IPv4Network(self.name)[0])
                self.end_ip = int(ipaddress.IPv4Network(self.name)[-1])
            else:
                raise ValidationError('\"' + self.name + '\" is not a valid ipv4 cidr address')

        if str(self.type) == "cidr6":
            try:
                ipaddress.IPv6Network(str(self.name))
            except:
                raise ValidationError('\"' + self.name + '\" is not a valid ipv6 cidr address')
            self.start_ip = int(ipaddress.IPv6Network(self.name)[0])
            self.end_ip = int(ipaddress.IPv6Network(self.name)[-1])

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
                    except:
                        raise ValidationError('\"' + ip4 + '\" is not a valid ipv4 address')
                self.start_ip = int(ipaddress.IPv4Address(pair[0]))
                self.end_ip = int(ipaddress.IPv4Address(pair[1]))
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
                    except:
                        raise ValidationError('\"' + ip6 + '\" is not a valid ipv6 address')
                self.start_ip = int(ipaddress.IPv6Address(pair[0]))
                self.end_ip = int(ipaddress.IPv6Address(pair[1]))
            else:
                raise ValidationError('\"' + self.name + '\" is not a valid range6 address, please use a hyphen as a separator eg 2001:db8::-2001:db8:0000:0000:0000:0000:0000:00ff')

        if str(self.type) == "netmask4":
            match = re.search('[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}/[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}', self.name,  )
            if match:
                try:
                    ipaddress.IPv4Network(str(self.name))
                except:
                    raise ValidationError('\"' + self.name + '\" is not a valid ipv4 netmask, please use forward slash as separator eg 192.168.10.0/255.255.255.0')
                self.start_ip = int(ipaddress.IPv4Network(self.name)[0])
                self.end_ip = int(ipaddress.IPv4Network(self.name)[-1])
            else:
                raise ValidationError('\"' + self.name + '\" is not a valid ipv4 netmask, please use forward slash as separator eg 192.168.10.0/255.255.255.0')

        if str(self.type) == "domain":
            test = validators.domain(self.name)
            if test != True:
                raise ValidationError('\"' + self.name + '\" is not a valid domain name')

            # remove old lookup results ready for new one
            comment = re.sub('^__.*$', '', self.comment, 0, re.MULTILINE)
            # remove blank lines
            comment = re.sub(r'^\s*$', '', comment, 0, re.MULTILINE)

            self.start_ip = 0
            self.end_ip = 0

            # move this code to an async task so the browser doesn't hang
            try:
                lookup = socket.gethostbyname_ex(self.name)
                hostname = lookup[0]
                aliases = re.sub('[\[\]\']', '', str(lookup[1]))
                ips = re.sub('[\[\]\']', '', str(lookup[2]))

                self.comment = \
                    comment + "\r\n" + \
                    "__hostname: " + hostname + "\r\n" + \
                    "__aliases: " + aliases + "\r\n" + \
                    "__ips: " + ips
            except:
                self.comment = comment + "\r\n" + "__iplookup failed for " + self.name

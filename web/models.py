from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.db import models
import ipaddress

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
                ipaddress.IPv4Address(str(self.name));
            except ValueError:
                raise ValidationError('\"' + self.name + '\" is not a valid ipv4 address')
        if str(self.type) == "ipv6":
            try:
                ipaddress.IPv6Address(str(self.name));
            except ValueError:
                raise ValidationError('\"' + self.name + '\" is not a valid ipv6 address')

    # def get_absolute_url(self):
    #     return reverse('asset-detail', kwargs={'pk': self.pk})

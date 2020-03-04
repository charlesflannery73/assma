from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Sector(models.Model):
    sector = models.CharField(max_length=255, null=False)

    def __str__(self):
        return self.sector


class Level(models.Model):
    level = models.CharField(max_length=255, null=False)

    def __str__(self):
        return self.level


class Org(models.Model):

    name = models.CharField(max_length=255, null=False)
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    tier = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], default=5)
    comment = models.TextField()
    created = models.DateTimeField(default=timezone.now)
    modified = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('org-detail', kwargs={'pk': self.pk})


class Asset(models.Model):
    type_enum = (
        (1, 'domain'),
        (2, 'ip4'),
        (3, 'range4'),
        (4, 'mask4'),
        (5, 'cidr4'),
        (6, 'range6'),
        (7, 'mask6'),
        (8, 'cidr6'),
    )

    name = models.CharField(max_length=255, null=False)
    org = models.ForeignKey(Org, on_delete=models.CASCADE)
    type = models.IntegerField(choices=type_enum, null=False)
    comment = models.TextField()
    created = models.DateTimeField(default=timezone.now)
    modified = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('asset-detail', kwargs={'pk': self.pk})

from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Org(models.Model):
    sector_enum = (
        (1, "Unknown"),
        (2, "Financial"),
        (3, "Government"),
        (4, "Energy"),
        (5, "Education"),
    )
    level_enum = (
        (1, 'Unknown'),
        (2, 'State'),
        (3, 'Federal'),
    )

    name = models.CharField(max_length=255, null=False)
    sector = models.IntegerField(choices=sector_enum, default=1)
    level = models.IntegerField(choices=level_enum, default=1)
    tier = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(6)], default=6)
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

from django.db import models
from .managers import PackageManager


class Package(models.Model):
    name = models.CharField(max_length=100)
    summary = models.TextField()
    description = models.TextField()
    point_of_contact = models.CharField(max_length=100)
    icon = models.CharField(max_length=100)
    upstream_url = models.CharField(max_length=100)

    objects = PackageManager()


class SubPackage(models.Model):
    name = models.CharField(max_length=100)
    summary = models.TextField()
    description = models.TextField()
    icon = models.CharField(max_length=100)
    package = models.ForeignKey(Package, related_name="subpkgs", on_delete=models.CASCADE)

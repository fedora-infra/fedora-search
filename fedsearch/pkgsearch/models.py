from django.db import models
from .managers import PackageManager


class Package(models.Model):
    name = models.CharField(max_length=100)
    summary = models.TextField(default="no summary", null=True)
    description = models.TextField(default="no description", null=True)
    point_of_contact = models.CharField(max_length=100)
    icon = models.CharField(max_length=100, default="package_128x128.png", null=True)
    upstream_url = models.CharField(max_length=150, default="no url", null=True)

    objects = PackageManager()


class SubPackage(models.Model):
    name = models.CharField(max_length=100)
    summary = models.TextField(default="no summary", null=True)
    description = models.TextField(default="no description", null=True)
    package = models.ForeignKey(Package, related_name="subpkgs", on_delete=models.CASCADE)

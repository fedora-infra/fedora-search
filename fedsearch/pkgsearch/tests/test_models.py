import pytest
from django.test import TestCase
from mixer.backend.django import mixer


from fedsearch.pkgsearch.models import Package, SubPackage

pytestmark = pytest.mark.django_db


class PackageTests(TestCase):
    def test_create(self):
        """Ensure we can create an instance of Package."""
        mixer.blend(Package)
        assert Package.objects.count() == 1

    def test_query(self):
        """Ensure we can query an instance of Package."""
        mixer.blend(
            Package,
            name="vim",
            summary="The VIM version of the vi editor for the X Window System - GVim",
        )
        r = Package.objects.filter(summary__contains="editor")
        for pkg in r.all():
            assert pkg.name == "vim"

    def test_query_subpkg(self):
        """Ensure we can query an instance of Package and get subpackages info"""
        pkg = mixer.blend(Package, name="gcc")
        mixer.blend(SubPackage, name="cpp", package=pkg)
        r = Package.objects.filter(name__contains="gcc")
        for pkg in r.all():
            assert pkg.name == "gcc"
            for subpkg in pkg.subpkgs.all():
                assert subpkg.name == "cpp"


class SubPackageTests(TestCase):
    def test_create(self):
        mixer.blend(SubPackage)
        assert SubPackage.objects.count() == 1

    def test_query(self):
        pkg = mixer.blend(Package, name="gcc")
        mixer.blend(SubPackage, name="cpp", package=pkg)
        r = SubPackage.objects.filter(name__contains="cpp")
        for subpkg in r.all():
            assert subpkg.name == "cpp"
            assert subpkg.package.name == "gcc"

import pytest
from django.test import TestCase
from mixer.backend.django import mixer


from fedsearch.pkgsearch.models import Package, SubPackage
from fedsearch.pkgsearch.tests.utils import create_pkgs

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

    def test_text_search_name(self):
        """Ensure we search a package using the name."""
        create_pkgs()
        r = Package.objects.search("tmux", unittest=True).values_list("name")
        expected = [("tmux",)]
        self.assertSequenceEqual(expected, r.all())

    def test_text_search_summary(self):
        """Ensure we search a package using the summary."""
        create_pkgs()
        r = Package.objects.search("terminal", unittest=True).values_list("name")
        expected = [("mate-terminal",), ("gnome-terminal",), ("tmux",)]
        self.assertSequenceEqual(expected, r.all())

    def test_text_search_description(self):
        """Ensure we search a package using the description."""
        create_pkgs()
        r = Package.objects.search("multiple", unittest=True).values_list("name")
        expected = [("mate-terminal",), ("gnome-terminal",)]
        self.assertSequenceEqual(expected, r.all())


class SubPackageTests(TestCase):
    def test_create(self):
        """Ensure we can create an instance of SubPackage."""
        mixer.blend(SubPackage)
        assert SubPackage.objects.count() == 1

    def test_query(self):
        """Ensure we can create an instance of SubPackage."""
        pkg = mixer.blend(Package, name="gcc")
        mixer.blend(SubPackage, name="cpp", package=pkg)
        r = SubPackage.objects.filter(name__contains="cpp")
        for subpkg in r.all():
            assert subpkg.name == "cpp"
            assert subpkg.package.name == "gcc"

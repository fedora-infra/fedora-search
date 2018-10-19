import pytest
from django.test import TestCase
from mixer.backend.django import mixer


from fedsearch.pkgsearch.models import Package, SubPackage

pytestmark = pytest.mark.django_db


class PackageTests(TestCase):
    def create_pkgs(self):
        """ Helper method used to create instances of the Packages object """
        Package.objects.get_or_create(
            name="mate-terminal",
            summary="Terminal emulator for MATE",
            description="Mate-terminal is a terminal emulator for MATE. \
            It supports translucent backgrounds, opening multiple terminals \
            in a single window (tabs) and clickable URLs.",
            point_of_contact="asterix",
            icon="",
            upstream_url="http://mate-desktop.org/",
        )
        Package.objects.get_or_create(
            name="gnome-terminal",
            summary="Terminal emulator for GNOME",
            description="gnome-terminal is a terminal emulator for GNOME. \
            It features the ability to use multiple terminals in a single window (tabs) \
            and profiles support.",
            point_of_contact="obelix",
            icon="",
            upstream_url="http://www.gnome.org/",
        )
        Package.objects.get_or_create(
            name="tmux",
            summary="A terminal multiplexer",
            description='tmux is a "terminal multiplexer." It enables a number of terminals \
            (or windows) to be accessed and controlled from a single terminal. tmux is intended \
            to be a simple, modern, BSD-licensed alternative to programs such as GNU Screen.',
            point_of_contact="idefix",
            icon="",
            upstream_url="https://tmux.github.io/",
        )

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
        self.create_pkgs()
        r = Package.objects.search("tmux").values_list("name")
        expected = [("tmux",)]
        self.assertSequenceEqual(expected, r.all())

    def test_text_search_summary(self):
        """Ensure we search a package using the summary."""
        self.create_pkgs()
        r = Package.objects.search("terminal").values_list("name")
        expected = [("mate-terminal",), ("gnome-terminal",), ("tmux",)]
        self.assertSequenceEqual(expected, r.all())

    def test_text_search_description(self):
        """Ensure we search a package using the description."""
        self.create_pkgs()
        r = Package.objects.search("multiple").values_list("name")
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

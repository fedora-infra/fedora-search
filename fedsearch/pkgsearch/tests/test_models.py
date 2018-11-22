import pytest
from django.test import TestCase

from fedsearch.pkgsearch.models import Package, SubPackage
from fedsearch.pkgsearch.tests.utils import create_pkgs

pytestmark = pytest.mark.django_db


class PackageTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        create_pkgs()

    def test_create(self):
        """Ensure we can create an instance of Package."""
        assert Package.objects.count() == 3

    def test_text_search_name(self):
        """Ensure we search a package using the name."""
        r = Package.objects.search("tmux", unittest=True).values_list("name")
        expected = [("tmux",)]
        self.assertSequenceEqual(expected, r.all())

    def test_text_search_summary(self):
        """Ensure we search a package using the summary."""
        r = Package.objects.search("terminal", unittest=True).values_list("name")
        expected = [("mate-terminal",), ("gnome-terminal",), ("tmux",)]
        self.assertSequenceEqual(expected, r.all())

    def test_text_search_description(self):
        """Ensure we search a package using the description."""
        r = Package.objects.search("multiple", unittest=True).values_list("name")
        expected = [("mate-terminal",), ("gnome-terminal",)]
        self.assertSequenceEqual(expected, r.all())


class SubPackageTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        create_pkgs()

    def test_create(self):
        """Ensure we can create an instance of SubPackage."""
        assert SubPackage.objects.count() == 1

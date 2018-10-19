import pytest
from django.test import TestCase
from mixer.backend.django import mixer


from fedsearch.pkgsearch.models import Package

pytestmark = pytest.mark.django_db


class PackageTests(TestCase):
    def test_create(self):
        mixer.blend(Package)
        assert Package.objects.count() == 1

    def test_query(self):
        mixer.blend(
            Package,
            name="vim",
            summary="The VIM version of the vi editor for the X Window System - GVim",
        )
        r = Package.objects.filter(summary__contains="editor")
        assert r.values()[0]["name"] == "vim"

from django.test import TestCase

from fedsearch.pkgsearch.models import Package, SubPackage
from fedsearch.pkgsearch.tests.utils import create_pkgs
from fedsearch.pkgsearch.serializers import PackageSerializer, SubPackageSerializer


class PackageSerializerTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        create_pkgs()

    def test_serialize(self):
        """ Ensure that we can serialize the Package object """
        package = Package.objects.get(name="mate-terminal")
        serializer = PackageSerializer(package)
        assert serializer.data["name"] == package.name
        assert serializer.data["icon"] == package.icon

    def test_deserialize_invalid(self):
        """ Ensure that serializer fails with invalid data """
        serializer = PackageSerializer(
            data={
                "name": "tmux",
                "summary": "A terminal multiplexer",
                "description": 'tmux is a "terminal multiplexer."',
                "point_of_contact": "idefix",
                "icon": None,
                "upstream_url": "https://tmux.github.io/",
            }
        )
        assert serializer.is_valid() is False

    def test_serialize_with_subpackages(self):
        """ Ensure that we serialize the Package object with a list
        of Subpackes """
        package = Package.objects.get(name="gnome-terminal")
        serializer = PackageSerializer(package)
        print(serializer.data["subpkgs"])
        assert serializer.data["subpkgs"][0]["name"] == package.subpkgs.first().name


class SubPackageSerializerTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        create_pkgs()

    def test_serialize(self):
        """ Ensure that we can serialize the SubPackage object """
        subpackage = SubPackage.objects.first()
        serializer = SubPackageSerializer(subpackage)
        assert serializer.data["name"] == subpackage.name
        assert serializer.data["summary"] == subpackage.summary

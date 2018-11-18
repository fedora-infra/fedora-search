from django.test import TestCase

from fedsearch.pkgsearch.serializers import PackageSerializer
from mixer.backend.django import mixer


class PackageSerializerTests(TestCase):
    def test_serialize(self):
        """ Ensure that we can serialize the Package object """
        package = mixer.blend("pkgsearch.Package")
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
        subpackage1 = mixer.blend("pkgsearch.SubPackage")
        subpackage2 = mixer.blend("pkgsearch.SubPackage")
        package = mixer.blend("pkgsearch.Package")
        package.subpkgs.add(subpackage1)
        package.subpkgs.add(subpackage2)
        serializer = PackageSerializer(package)
        print(serializer.data["subpkgs"])
        assert serializer.data["subpkgs"] == [subpackage2.name, subpackage1.name]

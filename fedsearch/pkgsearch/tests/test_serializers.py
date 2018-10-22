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

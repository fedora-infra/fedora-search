from rest_framework.serializers import ModelSerializer

from fedsearch.pkgsearch.models import Package, SubPackage


class SubPackageSerializer(ModelSerializer):
    class Meta:
        model = SubPackage
        fields = ["name", "summary", "description"]


class PackageSerializer(ModelSerializer):
    subpkgs = SubPackageSerializer(many=True)

    class Meta:
        model = Package
        fields = [
            "name",
            "summary",
            "description",
            "point_of_contact",
            "icon",
            "upstream_url",
            "subpkgs",
        ]

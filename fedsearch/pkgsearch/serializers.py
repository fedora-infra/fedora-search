from rest_framework.serializers import ModelSerializer, StringRelatedField

from fedsearch.pkgsearch.models import Package


class PackageSerializer(ModelSerializer):
    subpkgs = StringRelatedField(many=True)

    class Meta:
        model = Package
        fields = "__all__"

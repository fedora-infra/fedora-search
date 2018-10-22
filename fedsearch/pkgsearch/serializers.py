from rest_framework.serializers import ModelSerializer

from fedsearch.pkgsearch.models import Package


class PackageSerializer(ModelSerializer):
    class Meta:
        model = Package
        fields = "__all__"

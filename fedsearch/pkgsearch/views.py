from rest_framework.response import Response
from rest_framework.views import APIView

from fedsearch.pkgsearch.models import Package
from fedsearch.pkgsearch.serializers import PackageSerializer


class PackageSearchView(APIView):
    def get(self, request):
        query = request.query_params.get("q")
        queryset = Package.objects.search(query)
        results = []
        for pkg in queryset:
            serializer = PackageSerializer(pkg)
            results.append(serializer.data)
        return Response(results)

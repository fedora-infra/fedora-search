from rest_framework.views import APIView
from rest_framework.settings import api_settings

from fedsearch.pkgsearch.models import Package
from fedsearch.pkgsearch.serializers import PackageSerializer


class PackageSearchView(APIView):
    def get(self, request):
        pagination_class = api_settings.DEFAULT_PAGINATION_CLASS
        paginator = pagination_class()

        query = request.query_params.get("q")
        queryset = Package.objects.search(query)

        page = paginator.paginate_queryset(queryset, request)
        if page is not None:
            serializer = PackageSerializer(page, many=True)
            results = paginator.get_paginated_response(serializer.data)
        else:
            serializer = PackageSerializer(queryset, many=True)
            results = serializer.data

        return results

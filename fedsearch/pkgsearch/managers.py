from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.db import models

search_vectors = (
    SearchVector("name", weight="A", config="english")
    + SearchVector("summary", weight="D", config="english")
    + SearchVector("description", weight="D", config="english")
)


class PackageManager(models.Manager):
    def search(self, text):
        search_query = SearchQuery(text, config="english")
        search_rank = SearchRank(search_vectors, search_query)
        return (
            self.get_queryset()
            .annotate(search=search_vectors)
            .filter(search=search_query)
            .annotate(rank=search_rank)
            .order_by("-rank")
        )

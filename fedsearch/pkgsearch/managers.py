from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector, TrigramSimilarity
from django.db import models

search_vectors = (
    SearchVector("name", weight="A", config="english")
    + SearchVector("summary", weight="B", config="english")
    + SearchVector("description", weight="D", config="english")
)


class PackageManager(models.Manager):
    def search(self, text, unittest=False):
        search_query = SearchQuery(text, config="english")
        search_rank = SearchRank(search_vectors, search_query)
        trigram_similarity = TrigramSimilarity("name", text)

        # Disable the Trigram search if we are running unit test
        if unittest:
            trigram_similarity = None

        return (
            self.get_queryset()
            .annotate(search=search_vectors)
            .filter(search=search_query)
            .annotate(rank=search_rank + trigram_similarity)
            .order_by("-rank")
        )

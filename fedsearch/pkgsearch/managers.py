from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector, TrigramSimilarity
from django.db import models


class PackageManager(models.Manager):
    def search(self, text, unittest=False):
        search_query = SearchQuery(text, config="english")
        search_rank = SearchRank(models.F("search_vector"), search_query)
        trigram_similarity = TrigramSimilarity("name", text)

        # Disable the Trigram search if we are running unit test
        if unittest:
            trigram_similarity = None

        return (
            self.get_queryset()
            .annotate(rank=search_rank + trigram_similarity)
            .filter(search_vector=search_query)
            .order_by("-rank")
        )

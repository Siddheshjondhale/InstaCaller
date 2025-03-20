from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.postgres.search import SearchQuery, SearchRank, TrigramSimilarity
from django.db.models import Q
from globalcontacts.models import GlobalContactPhoneBook

# Search By Name or By Phone Number (Using Redis cache for caching)
class SearchView(APIView):
    def get(self, request):
        query = request.GET.get("query", "").strip()

        if not query:
            return Response({"message": "No search query provided"}, status=400)

        cache_key = f"search_{query.lower()}"
        cached_result = cache.get(cache_key)

        if cached_result:
            print("fetched from the redis cache "+ str(cached_result))
            return Response(cached_result)

        contacts = GlobalContactPhoneBook.objects.none()

        if query.isdigit():
            # search by phone number
            contacts = GlobalContactPhoneBook.objects.filter(
                Q(phone_number=query) | Q(phone_number=f"+{query}")
            )
        else:
            # fulltext search for name searches
            search_query = SearchQuery(query)
            contacts = GlobalContactPhoneBook.objects.annotate(
                rank=SearchRank("search_vector", search_query),
                similarity=TrigramSimilarity("name", query)
            ).filter(Q(search_vector=search_query) | Q(similarity__gt=0.3)).order_by("-rank", "-similarity")

        result = [
            {
                "name": contact.name,
                "phone_number": contact.phone_number,
                "is_registered": contact.is_registered,
                "spam_reports": 0
            }
            for contact in contacts
        ]

        if not result:
            return Response({"message": "No contacts found matching your query"}, status=404)

        # store the result in redis cache for temporary duration (5 mins)
        cache.set(cache_key, result, timeout=300)

        return Response(result)

from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.postgres.search import SearchQuery, SearchRank, TrigramSimilarity
from django.db.models import Q
from globalcontacts.models import GlobalContactPhoneBook
from spammanagement.models import SpamSummary 

# Search By Name or By Phone Number (Using Redis cache for caching)
class SearchContactView(APIView):
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

        result = []
        for contact in contacts:
            # Get spam count from SpamSummary
            spam_summary = SpamSummary.objects.filter(phone_number=contact.phone_number).first()
            spam_count = spam_summary.spam_count if spam_summary else 0

            result.append({
                "name": contact.name,
                "phone_number": contact.phone_number,
                "is_registered": contact.is_registered,
                "spam_reports": spam_count  # Include the spam count here
            })

        if not result:
            return Response({"message": "No contacts found matching your query"}, status=404)

        # store the result in redis cache for temporary duration (5 mins)
        cache.set(cache_key, result, timeout=300)

        return Response(result)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.core.cache import cache
from django.contrib.postgres.search import SearchVector
from globalcontacts.models import GlobalContactPhoneBook
from .models import SpamReport, SpamSummary

# Submit A Spam report
class ReportSpamView(APIView):
    def post(self, request):
        phone_number = request.data.get("phone_number", "")
        spammer_name = request.data.get("spammer_name", "")
        reason = request.data.get("reason", "")

        if not phone_number:
            return Response({"error": "Phone number is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                SpamReport.objects.create(
                    phone_number=phone_number,
                    reason=reason,
                    spammer_name=spammer_name
                )
                spam_count = SpamSummary.update_summary(phone_number)

                contact,created = GlobalContactPhoneBook.objects.get_or_create(
                    phone_number=phone_number,
                    name=spammer_name,
                    is_registered=False
                )

                contact.search_vector = SearchVector("name")
                contact.save()

            cache.delete(f"spam_summary_{phone_number}")

            return Response({
                "message": "Spam report submitted successfully",
                "spam_count": spam_count
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": f"Failed to update spam summary: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Summary of Spam reports done 
class SpamSummaryView(APIView):
    def get(self, request):
        phone_number = request.GET.get("phone_number", "").strip()
        
        if not phone_number:
            return Response({"error": "Phone number is required"}, status=status.HTTP_400_BAD_REQUEST)

        cache_key = f"spam_summary_{phone_number}"
        cached_summary = cache.get(cache_key)

        if cached_summary:
            return Response(cached_summary, status=status.HTTP_200_OK)

        if not phone_number.startswith('+'):
            phone_number = f"+{phone_number}"

        summary = SpamSummary.objects.filter(phone_number=phone_number).first()
        spam_count = summary.spam_count if summary else 0

        response_data = {
            "phone_number": phone_number,
            "spam_count": spam_count
        }

        cache.set(cache_key, response_data, timeout=300)
        return Response(response_data, status=status.HTTP_200_OK)

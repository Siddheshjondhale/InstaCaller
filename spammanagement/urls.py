from django.urls import path
from .views import ReportSpamView, SpamSummaryView

urlpatterns = [
    path("report/", ReportSpamView.as_view(), name="report_spam"),
    path("summary/", SpamSummaryView.as_view(), name="spam_summary"),
]

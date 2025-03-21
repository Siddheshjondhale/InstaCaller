from django.contrib import admin

from spammanagement.models import SpamReport, SpamSummary

admin.site.register(SpamReport)
admin.site.register(SpamSummary)    
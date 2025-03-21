from rest_framework import serializers
from .models import SpamReport

class SpamReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpamReport
        fields = ["phone_number", "reason", "created_at"]

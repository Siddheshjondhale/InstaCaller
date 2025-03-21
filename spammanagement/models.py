from venv import logger
from django.db import models

class SpamReport(models.Model):
    phone_number = models.CharField(max_length=20, db_index=True)
    reason = models.TextField(null=True, blank=True)
    spammer_name = models.CharField(max_length=255, null=True, blank=True)   
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "spam_reports"
        indexes = [models.Index(fields=["phone_number"])]  

    def __str__(self):
        return f"{self.phone_number} reported as spam"

class SpamSummary(models.Model):
    phone_number = models.CharField(max_length=20, unique=True, db_index=True)  # Indexing for phone number
    spam_count = models.IntegerField(default=0)
    last_reported_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "spam_summary"
        indexes = [models.Index(fields=["phone_number"])]

    @classmethod
    def update_summary(cls, phone_number):
        count = SpamReport.objects.filter(phone_number=phone_number).count()

        obj, created = cls.objects.update_or_create(
            phone_number=phone_number,
            defaults={"spam_count": count}
        )

        if created:
            logger.info(f"New SpamSummary created for {phone_number} with count {count}")
        else:
            logger.info(f"SpamSummary updated for {phone_number}: {count}")

        return obj.spam_count

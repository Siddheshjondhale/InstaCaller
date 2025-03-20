from django.db import models
from users.models import UserProfile
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVector, SearchVectorField
from django.contrib.postgres.search import SearchVector

class GlobalContactPhoneBook(models.Model):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, db_index=True)
    registered_user_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True)
    is_registered = models.BooleanField(default=False)
    search_vector = SearchVectorField(null=True)

    class Meta:
        db_table = "globalcontacts" 

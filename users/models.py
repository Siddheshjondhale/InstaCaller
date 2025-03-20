from django.db import models
import uuid
from django.contrib.auth.models import AbstractBaseUser  # user authentication

# user registration model 
class UserProfile(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone_number = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, null=True, blank=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["name"]
    last_login=None   # Removing last_login column 

    def save(self, *args, **kwargs):
        #
        if self.password and not self.password.startswith("pbkdf2_sha256$"):
            from django.contrib.auth.hashers import make_password
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    class Meta:
        db_table = "user_profiles"  # table name for storing registred users

    def __str__(self):
        return f"{self.name} ({self.phone_number})"

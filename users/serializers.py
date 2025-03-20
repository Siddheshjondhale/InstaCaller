from globalcontacts.models import GlobalContactPhoneBook
from .models import UserProfile
from rest_framework import serializers
from django.contrib.postgres.search import SearchVector

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["id", "phone_number", "name", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}  # Setting password field write only and restrict the read only

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = UserProfile(**validated_data)
        user.set_password(password)
        user.save()

        # add the registered user to globalcontacts table for searching purpose
        contact = GlobalContactPhoneBook.objects.create(
            phone_number=user.phone_number,
            name=user.name,
            registered_user_id=user,
            is_registered=True
        )

        GlobalContactPhoneBook.objects.filter(id=contact.id).update(
            search_vector=SearchVector("name")
        )

        return user

from .models import UserProfile
from rest_framework import serializers
from django.contrib.auth.hashers import check_password

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserProfile
        fields = ["id", "phone_number", "name", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}   # Setting password field write only and restrict the read only

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = UserProfile(**validated_data)
        user.set_password(password)
        user.save()
        return user

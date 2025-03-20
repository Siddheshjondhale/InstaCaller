from rest_framework import generics
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import UserProfile


class RegisterView(generics.CreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs) 
        user = UserProfile.objects.get(phone_number=response.data["phone_number"])

        refresh = RefreshToken.for_user(user)

        return Response({
            "message":"Registration Success",
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh)
        })
    

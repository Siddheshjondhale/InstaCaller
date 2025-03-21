from rest_framework_simplejwt.authentication import JWTAuthentication
from django.utils.deprecation import MiddlewareMixin
from rest_framework.response import Response
from django.http import JsonResponse

class JWTBearerAuthMiddleware(MiddlewareMixin):
    PUBLIC_PATHS = ["/api/users/register/"]  # Allowing public paths without JWT auth

    def process_request(self, request):
        if request.path in self.PUBLIC_PATHS:
            return

        auth = JWTAuthentication()
        header = auth.get_header(request)

        if not header or not header.startswith(b"Bearer "):
            return JsonResponse({"error": "Authentication failed. Please provide a valid token"}, status=401)

        try:
            print(f"Header received: {header}")
            token = header[7:].decode()
            validated_token = auth.get_validated_token(token)
            request.user = auth.get_user(validated_token)
            print(f"Validated user: {request.user}")
            

        except Exception as e:
            print(f"JWT Authentication Error: {str(e)}")  # Print actual error for debugging
            return JsonResponse({"error": "Invalid or expired token. Please log in again"}, status=401)

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/users/", include("users.urls")),
    path("api/globalcontacts/", include("globalcontacts.urls")),
    path("api/spam/", include("spammanagement.urls")),
]
